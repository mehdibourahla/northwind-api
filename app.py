from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, inspect
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@db:5432/northwind"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

def validate_sql(query):
    """Basic SQL validation to prevent dangerous operations"""
    if not query.strip().lower().startswith('select'):
        return False
    
    forbidden_keywords = ['drop', 'delete', 'insert', 'update', 'alter', 'truncate']
    for keyword in forbidden_keywords:
        if re.search(rf"\b{keyword}\b", query, re.IGNORECASE):
            return False
    return True

@app.route('/schema', methods=['GET'])
def get_schema():
    """Get the database schema including tables and their columns with types"""
    inspector = inspect(db.engine)
    schema = {}
    
    for table_name in inspector.get_table_names():
        columns = []
        for column in inspector.get_columns(table_name):
            columns.append({
                'name': column['name'],
                'type': str(column['type']),
                'nullable': column['nullable']
            })
        schema[table_name] = columns
    
    return jsonify(schema)



@app.route('/query', methods=['POST'])
def execute_query():
    """Execute a SQL query and return the results"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "No query provided"}), 400
            
        query = data['query']
        if not validate_sql(query):
            return jsonify({"error": "Invalid or forbidden SQL query"}), 400

        result = db.session.execute(text(query))
        rows = result.fetchall()
        return jsonify([dict(row._mapping) for row in rows])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)