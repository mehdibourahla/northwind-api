import os
import sys
import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def execute_command(command):
    """Execute a shell command and print output"""
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
        stdout, stderr = process.communicate()
        
        if stdout:
            print(stdout.decode())
        if stderr:
            print(stderr.decode(), file=sys.stderr)
            
        return process.returncode == 0
    except Exception as e:
        print(f"Error executing command: {e}", file=sys.stderr)
        return False

def create_database():
    """Create the Northwind database"""
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Drop database if exists
        cursor.execute("DROP DATABASE IF EXISTS northwind;")
        print("Dropped existing northwind database if it existed.")
        
        # Create database
        cursor.execute("CREATE DATABASE northwind;")
        print("Created new northwind database.")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error creating database: {e}", file=sys.stderr)
        return False

def load_data():
    """Load the Northwind schema and data"""
    try:
        # Load the SQL file into the database
        command = "psql -U postgres -d northwind -f northwind.sql"
        if not execute_command(command):
            raise Exception("Failed to load database schema and data")
            
        print("Successfully loaded database schema and data.")
        return True
        
    except Exception as e:
        print(f"Error loading data: {e}", file=sys.stderr)
        return False

def verify_database():
    """Verify the database was created successfully"""
    try:
        conn = psycopg2.connect(
            dbname="northwind",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
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

def main():
    print("Starting Northwind database setup...")
    
    if not create_database():
        print("Failed to create database. Exiting.")
        sys.exit(1)
        
    if not load_data():
        print("Failed to load data. Exiting.")
        sys.exit(1)
        
    if not verify_database():
        print("Failed to verify database. Exiting.")
        sys.exit(1)
        
    print("\nNorthwind database setup completed successfully!")

if __name__ == "__main__":
    main()