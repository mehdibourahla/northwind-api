import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DATABASE_NAME = "northwind"

def database_exists(conn, dbname):
    """Check if a database exists"""
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s;", (dbname,))
    exists = cursor.fetchone() is not None
    cursor.close()
    return exists

def create_database():
    """Create the Northwind database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server with the default database (postgres)
        conn = psycopg2.connect(
            dbname="postgres",
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "password"),
            host=os.getenv("DB_HOST"),  # Cloud SQL connection string or IP
            port=os.getenv("DB_PORT", "5432")
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        # Check if the database already exists
        if database_exists(conn, DATABASE_NAME):
            print(f"Database {DATABASE_NAME} already exists. Aborting setup.")
            conn.close()
            return False

        cursor = conn.cursor()

        # Create the database
        cursor.execute(f"CREATE DATABASE {DATABASE_NAME};")
        print(f"Created new {DATABASE_NAME} database.")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Error creating database: {e}", file=sys.stderr)
        return False

def load_data():
    """Load schema and data directly from SQL commands"""
    try:
        # Connect to the newly created Northwind database
        conn = psycopg2.connect(
            dbname=DATABASE_NAME,
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "password"),
            host=os.getenv("DB_HOST"),  # Cloud SQL connection string or IP
            port=os.getenv("DB_PORT", "5432")
        )
        cursor = conn.cursor()

        # Load schema and data from a SQL file
        with open("northwind.sql", "r") as file:
            sql_commands = file.read()
            cursor.execute(sql_commands)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Successfully loaded database schema and data.")
        return True

    except Exception as e:
        print(f"Error loading data: {e}", file=sys.stderr)
        return False

def verify_database():
    """Verify the database was created successfully"""
    try:
        conn = psycopg2.connect(
            dbname=DATABASE_NAME,
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "password"),
            host=os.getenv("DB_HOST", "/cloudsql/infinitgraphprototype:us-central1:northwind"),  # Cloud SQL connection string or IP
            port=os.getenv("DB_PORT", "5432")
        )
        cursor = conn.cursor()

        # Check for some key tables
        tables = [
            "customers",
            "employees",
            "orders",
            "products",
            "suppliers"
        ]

        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"Table {table}: {count} records")

        cursor.close()
        conn.close()
        print("\nDatabase verification completed successfully.")
        return True

    except Exception as e:
        print(f"Error verifying database: {e}", file=sys.stderr)
        return False

def setup_database():
    print("Starting Northwind database setup...")

    if not create_database():
        print("Database setup aborted or failed to create database. Exiting.")
        sys.exit(1)

    if not load_data():
        print("Failed to load data. Exiting.")
        sys.exit(1)

    if not verify_database():
        print("Failed to verify database. Exiting.")
        sys.exit(1)

    print("\nNorthwind database setup completed successfully!")

