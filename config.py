import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_HOST = os.getenv('DB_HOST', 'localhost')  # Default to localhost if not set
DATABASE_NAME = os.getenv('DB_NAME', 'ecommerce_analytics')
DATABASE_USER = os.getenv('DB_USER', 'postgres')
DATABASE_PASSWORD = os.getenv('DB_PASSWORD')  # No default - must be set!
DATABASE_PORT = int(os.getenv('DB_PORT', 5432))

#paths
DATA_FILE = os.getenv('DATA_FILE', 'data/data.csv')
BATCH_SIZE = int(os.getenv('BATCH_SIZE', 10000))

#config dictionary
DB_CONFIG = {
    'host': DATABASE_HOST,
    'database': DATABASE_NAME,
    'user': DATABASE_USER,
    'password': DATABASE_PASSWORD,
    'port': DATABASE_PORT
}

def validate_config():
    """Check if all required settings are present"""
    if not DATABASE_PASSWORD:
        raise ValueError("DB_PASSWORD must be set in .env file!")
    
    if not os.path.exists(DATA_FILE):
        print(f"Warning: Data file not found: {DATA_FILE}")
    
    print("Configuration validation passed!")

if __name__ == "__main__":
    print("Configuration loaded!")
    print(f"Database: {DATABASE_NAME}")
    print(f"Data file: {DATA_FILE}")
    
    try:
        validate_config()
    except ValueError as e:
        print(f"Configuration error: {e}")