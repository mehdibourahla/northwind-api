# Northwind Database API

A simple Flask API that provides access to the Northwind database with SQL query capabilities.

## Features

- Get complete database schema
- Execute SQL queries against the database
- Docker containerized application
- CORS enabled
- SQL injection protection

## Prerequisites

- Docker and Docker Compose
- Git
- PostgreSQL client (for local database setup)

## Project Structure

```
northwind-api/
├── app.py                 # Main Flask application
├── setup_database.py      # Database setup script
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration for the Flask app
├── docker-compose.yml    # Docker Compose configuration
├── northwind.sql         # Database schema and data
└── README.md            # This file
```

## Setup and Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd northwind-api
```

### 2. Local Database Setup (Optional - Skip if using Docker)

If you want to set up the database locally without Docker:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the database setup script
python setup_database.py
```

### 3. Docker Setup (Recommended)

Build and run the application using Docker Compose:

```bash
# Build and start the containers
docker-compose up --build

# To run in detached mode
docker-compose up -d --build
```

The application will be available at `http://localhost:5000`

## API Endpoints

### 1. Get Database Schema

```http
GET /schema
```

Returns a JSON object containing all tables and their column definitions.

### 2. Execute SQL Query

```http
POST /query
Content-Type: application/json

{
    "query": "SELECT * FROM customers LIMIT 5"
}
```

Only SELECT queries are allowed for security reasons.

## Example Usage

### Using cURL

1. Get Schema:

```bash
curl http://localhost:5000/schema
```

2. Execute Query:

```bash
curl -X POST http://localhost:5000/query \
     -H "Content-Type: application/json" \
     -d '{"query": "SELECT * FROM customers LIMIT 5"}'
```

### Using Python requests

```python
import requests

# Get schema
schema_response = requests.get('http://localhost:5000/schema')
print(schema_response.json())

# Execute query
query = {
    "query": "SELECT * FROM customers LIMIT 5"
}
query_response = requests.post('http://localhost:5000/query', json=query)
print(query_response.json())
```

## Security

- Only SELECT queries are allowed
- Basic SQL injection protection is implemented
- Forbidden keywords are blocked (DROP, DELETE, INSERT, UPDATE, etc.)

## Troubleshooting

1. If the database container fails to start:

```bash
# Check the logs
docker-compose logs db

# Recreate the containers
docker-compose down -v
docker-compose up --build
```

2. If the web application fails to connect to the database:

```bash
# Check if the database container is running
docker ps

# Check the web application logs
docker-compose logs web
```

3. If you need to reset the database:

```bash
# Stop all containers and remove volumes
docker-compose down -v

# Rebuild and start
docker-compose up --build
```

## Development

To make changes to the application:

1. Modify the code
2. Rebuild the containers:

```bash
docker-compose down
docker-compose up --build
```

## Environment Variables

The following environment variables can be modified in the `docker-compose.yml` file:

- `POSTGRES_USER`: Database username (default: postgres)
- `POSTGRES_PASSWORD`: Database password (default: postgres)
- `POSTGRES_DB`: Database name (default: northwind)
- `FLASK_ENV`: Flask environment (default: development)
