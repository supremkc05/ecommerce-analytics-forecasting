import psycopg2
from psycopg2 import sql
from config import DB_CONFIG
import sys

def create_connection():
    """
    Create a connection to PostgreSQL database
    Returns connection object or None if failed
    """
    config = DB_CONFIG
    
    try:
        # Create connection string
        connection = psycopg2.connect(
            host=config['host'],
            database=config['database'],
            user=config['user'],
            password=config['password'],
            port=config['port']
        )
        
        print("Successfully connected to PostgreSQL!")
        return connection
        
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def test_connection():
    """
    Test the database connection and show some basic info
    """
    conn = create_connection()
    
    if conn:
        try:
            # Create a cursor
            cursor = conn.cursor()
            
            # Test query - get PostgreSQL version
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"PostgreSQL version: {version[0]}")
            
            # List existing databases
            cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
            databases = cursor.fetchall()
            print("\nAvailable databases:")
            for db in databases:
                print(f"  - {db[0]}")
            
            cursor.close()
            conn.close()
            print("\nConnection test completed successfully!")
            
        except psycopg2.Error as e:
            print(f"Error testing connection: {e}")
            if conn:
                conn.close()
    else:
        print("Could not establish connection")

if __name__ == "__main__":
    print("=== Database Connection Test ===")
    test_connection()