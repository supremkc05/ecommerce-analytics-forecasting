import pandas as pd
import psycopg2
from urllib.parse import quote_plus
import logging
import sys
import os
from pathlib import Path

#parent directories for path
sys.path.append(str(Path(__file__).parent.parent / "database"))
sys.path.append(str(Path(__file__).parent.parent.parent))

from database.config import DB_CONFIG, DATA_FILE

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RobustETL:
    def __init__(self):
        """Initialize ETL process with database connection"""
        self.conn = None
        self.data = None
        
    def connect_to_database(self):
        """Connect to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.conn.autocommit = False
            logger.info("Connected to PostgreSQL database successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False
    
    def extract_data(self):
        """EXTRACT: Read data from CSV file"""
        try:
            logger.info("Starting data extraction...")
            
            # Read CSV file
            self.data = pd.read_csv(DATA_FILE)
            logger.info(f"Extracted {len(self.data)} rows from {DATA_FILE}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to extract data: {e}")
            return False
    
    def transform_data(self):
        """TRANSFORM: Clean and prepare data"""
        try:
            logger.info("Starting data transformation...")
            
            # Clean data
            original_rows = len(self.data)
            self.data = self.data.dropna(subset=['CustomerID', 'StockCode'])
            logger.info(f"Removed {original_rows - len(self.data)} rows with missing data")
            
            # Convert data types
            self.data['InvoiceDate'] = pd.to_datetime(self.data['InvoiceDate'])
            self.data['CustomerID'] = self.data['CustomerID'].astype(int)
            self.data['Quantity'] = pd.to_numeric(self.data['Quantity'], errors='coerce')
            self.data['UnitPrice'] = pd.to_numeric(self.data['UnitPrice'], errors='coerce')
            
            # Ensure InvoiceNo is string type consistently
            self.data['InvoiceNo'] = self.data['InvoiceNo'].astype(str)
            
            # Filter valid transactions (remove any rows with NaN values)
            self.data = self.data.dropna(subset=['InvoiceNo', 'CustomerID', 'Quantity', 'UnitPrice', 'TotalPrice'])
            self.data = self.data[
                (self.data['Quantity'] > 0) & 
                (self.data['UnitPrice'] > 0) &
                (self.data['TotalPrice'] > 0)
            ]
            
            # Create customers table
            self.customers = self.data.groupby('CustomerID').agg({
                'InvoiceDate': ['min', 'max'],
                'TotalPrice': ['sum', 'count']
            }).round(2)
            
            self.customers.columns = ['first_purchase_date', 'last_purchase_date', 'total_spent', 'total_orders']
            self.customers = self.customers.reset_index()
            self.customers.rename(columns={'CustomerID': 'customer_id'}, inplace=True)
            self.customers['avg_order_value'] = (self.customers['total_spent'] / self.customers['total_orders']).round(2)
            
            # Create products table
            self.products = self.data.groupby('StockCode').agg({
                'Description': 'first',
                'UnitPrice': 'mean',
                'InvoiceDate': 'min'
            }).round(2)
            
            self.products.columns = ['description', 'unit_price', 'first_seen_date']
            self.products = self.products.reset_index()
            self.products.rename(columns={'StockCode': 'stock_code'}, inplace=True)
            
            # Create orders table
            self.orders = self.data.groupby(['InvoiceNo', 'CustomerID']).agg({
                'InvoiceDate': 'first',
                'Country': 'first',
                'TotalPrice': 'sum',
                'Quantity': 'sum'
            }).round(2)
            
            self.orders.columns = ['invoice_date', 'country', 'total_amount', 'total_items']
            self.orders = self.orders.reset_index()
            self.orders.rename(columns={
                'InvoiceNo': 'invoice_no',
                'CustomerID': 'customer_id'
            }, inplace=True)
            
            # Create order_items table (ensure consistency with orders)
            self.order_items = self.data[[
                'InvoiceNo', 'StockCode', 'Quantity', 'UnitPrice', 'TotalPrice'
            ]].copy()
            
            self.order_items.rename(columns={
                'InvoiceNo': 'invoice_no',
                'StockCode': 'stock_code',
                'Quantity': 'quantity',
                'UnitPrice': 'unit_price',
                'TotalPrice': 'total_price'
            }, inplace=True)
            
            # Ensure order_items only contains valid references
            valid_invoices = set(self.orders['invoice_no'])
            valid_products = set(self.products['stock_code'])
            
            self.order_items = self.order_items[
                (self.order_items['invoice_no'].isin(valid_invoices)) &
                (self.order_items['stock_code'].isin(valid_products))
            ]
            logger.info(f"Filtered order_items to {len(self.order_items)} items with valid references")
            
            # Create transactions table (ensure referential integrity)
            self.transactions = self.data[[
                'InvoiceNo', 'StockCode', 'CustomerID', 'Quantity', 
                'UnitPrice', 'TotalPrice', 'InvoiceDate', 'Country'
            ]].copy()
            
            self.transactions.rename(columns={
                'InvoiceNo': 'invoice_no',
                'StockCode': 'stock_code',
                'CustomerID': 'customer_id',
                'Quantity': 'quantity',
                'UnitPrice': 'unit_price',
                'TotalPrice': 'total_price',
                'InvoiceDate': 'invoice_date',
                'Country': 'country'
            }, inplace=True)
            
            # Ensure referential integrity for transactions
            valid_customers = set(self.customers['customer_id'])
            valid_products = set(self.products['stock_code'])
            
            self.transactions = self.transactions[
                (self.transactions['customer_id'].isin(valid_customers)) &
                (self.transactions['stock_code'].isin(valid_products))
            ]
            logger.info(f"Filtered transactions to {len(self.transactions)} records with valid references")
            
            logger.info("Data transformation completed")
            logger.info(f"Prepared: {len(self.customers)} customers, {len(self.products)} products, {len(self.orders)} orders, {len(self.order_items)} order items, {len(self.transactions)} transactions")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to transform data: {e}")
            return False
    
    def clear_tables(self):
        """Clear existing data from tables"""
        try:
            cursor = self.conn.cursor()
            
            # Clear in proper order to respect foreign keys
            tables_to_clear = ['order_items', 'orders', 'transactions', 'products', 'customers']
            
            for table in tables_to_clear:
                cursor.execute(f"DELETE FROM {table}")
                logger.info(f"Cleared {table} table")
            
            self.conn.commit()
            cursor.close()
            logger.info("All tables cleared successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to clear tables: {e}")
            self.conn.rollback()
            return False
    
    def load_customers(self):
        """Load customers with batch commits"""
        try:
            logger.info(f"Loading {len(self.customers)} customers...")
            cursor = self.conn.cursor()
            
            batch_size = 100
            loaded = 0
            
            for i in range(0, len(self.customers), batch_size):
                batch = self.customers.iloc[i:i+batch_size]
                
                for _, row in batch.iterrows():
                    cursor.execute("""
                        INSERT INTO customers (customer_id, first_purchase_date, last_purchase_date, total_spent, total_orders, avg_order_value)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        int(row['customer_id']),
                        row['first_purchase_date'].date(),
                        row['last_purchase_date'].date(),
                        float(row['total_spent']),
                        int(row['total_orders']),
                        float(row['avg_order_value'])
                    ))
                
                # Commit each batch
                self.conn.commit()
                loaded += len(batch)
                
                if loaded % 500 == 0:
                    logger.info(f"Loaded {loaded} / {len(self.customers)} customers...")
            
            cursor.close()
            logger.info(f"Successfully loaded {loaded} customers")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load customers: {e}")
            self.conn.rollback()
            return False
    
    def load_products(self):
        """Load products with batch commits"""
        try:
            logger.info(f"Loading {len(self.products)} products...")
            cursor = self.conn.cursor()
            
            batch_size = 100
            loaded = 0
            
            for i in range(0, len(self.products), batch_size):
                batch = self.products.iloc[i:i+batch_size]
                
                for _, row in batch.iterrows():
                    cursor.execute("""
                        INSERT INTO products (stock_code, description, unit_price, first_seen_date)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        str(row['stock_code']),
                        str(row['description'])[:500] if pd.notna(row['description']) else '',  # Limit description length
                        float(row['unit_price']),
                        row['first_seen_date'].date()
                    ))
                
                # Commit each batch
                self.conn.commit()
                loaded += len(batch)
                
                if loaded % 500 == 0:
                    logger.info(f"Loaded {loaded} / {len(self.products)} products...")
            
            cursor.close()
            logger.info(f"Successfully loaded {loaded} products")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load products: {e}")
            self.conn.rollback()
            return False
    
    def load_orders(self):
        """Load orders with batch commits"""
        try:
            logger.info(f"Loading {len(self.orders)} orders...")
            cursor = self.conn.cursor()
            
            batch_size = 200
            loaded = 0
            
            for i in range(0, len(self.orders), batch_size):
                batch = self.orders.iloc[i:i+batch_size]
                
                for _, row in batch.iterrows():
                    cursor.execute("""
                        INSERT INTO orders (invoice_no, customer_id, invoice_date, country, total_amount, total_items)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        str(row['invoice_no']),
                        int(row['customer_id']),
                        row['invoice_date'].date(),
                        str(row['country']) if pd.notna(row['country']) else '',
                        float(row['total_amount']),
                        int(row['total_items'])
                    ))
                
                # Commit each batch
                self.conn.commit()
                loaded += len(batch)
                
                if loaded % 1000 == 0:
                    logger.info(f"Loaded {loaded} / {len(self.orders)} orders...")
            
            cursor.close()
            logger.info(f"Successfully loaded {loaded} orders")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load orders: {e}")
            self.conn.rollback()
            return False
    
    def load_order_items(self):
        """Load order items with batch commits"""
        try:
            logger.info(f"Loading {len(self.order_items)} order items...")
            cursor = self.conn.cursor()
            
            batch_size = 1000
            loaded = 0
            
            for i in range(0, len(self.order_items), batch_size):
                batch = self.order_items.iloc[i:i+batch_size]
                
                for _, row in batch.iterrows():
                    cursor.execute("""
                        INSERT INTO order_items (invoice_no, stock_code, quantity, unit_price, total_price)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        str(row['invoice_no']),
                        str(row['stock_code']),
                        int(row['quantity']),
                        float(row['unit_price']),
                        float(row['total_price'])
                    ))
                
                # Commit each batch
                self.conn.commit()
                loaded += len(batch)
                
                if loaded % 10000 == 0:
                    logger.info(f"Loaded {loaded} / {len(self.order_items)} order items...")
            
            cursor.close()
            logger.info(f"Successfully loaded {loaded} order items")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load order items: {e}")
            self.conn.rollback()
            return False
    
    def load_transactions(self):
        """Load transactions with batch commits"""
        try:
            logger.info(f"Loading {len(self.transactions)} transactions...")
            cursor = self.conn.cursor()
            
            batch_size = 1000
            loaded = 0
            
            for i in range(0, len(self.transactions), batch_size):
                batch = self.transactions.iloc[i:i+batch_size]
                
                for _, row in batch.iterrows():
                    cursor.execute("""
                        INSERT INTO transactions (invoice_no, stock_code, customer_id, quantity, unit_price, total_price, invoice_date, country)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        str(row['invoice_no']),
                        str(row['stock_code']),
                        int(row['customer_id']),
                        int(row['quantity']),
                        float(row['unit_price']),
                        float(row['total_price']),
                        row['invoice_date'],
                        str(row['country']) if pd.notna(row['country']) else ''
                    ))
                
                # Commit each batch
                self.conn.commit()
                loaded += len(batch)
                
                if loaded % 10000 == 0:
                    logger.info(f"Loaded {loaded} / {len(self.transactions)} transactions...")
            
            cursor.close()
            logger.info(f"Successfully loaded {loaded} transactions")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load transactions: {e}")
            self.conn.rollback()
            return False
    
    def validate_data(self):
        """Validate loaded data"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM customers")
            customers_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM products")
            products_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM orders")
            orders_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM order_items")
            order_items_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM transactions")
            transactions_count = cursor.fetchone()[0]
            
            cursor.close()
            
            logger.info("Data validation results:")
            logger.info(f"Customers: {customers_count:,}")
            logger.info(f"Products: {products_count:,}")
            logger.info(f"Orders: {orders_count:,}")
            logger.info(f"Order Items: {order_items_count:,}")
            logger.info(f"Transactions: {transactions_count:,}")
            
            return all([customers_count > 0, products_count > 0, orders_count > 0, order_items_count > 0, transactions_count > 0])
            
        except Exception as e:
            logger.error(f"Failed to validate data: {e}")
            return False
    
    def run_etl(self):
        """Run the ETL process with better error handling"""
        logger.info("Starting Robust ETL Pipeline...")
        logger.info("=" * 50)
        
        try:
            # Step 1
            if not self.connect_to_database():
                return False
            
            # Step 2
            if not self.extract_data():
                return False
            
            # Step 3
            if not self.transform_data():
                return False
            
            # Step 4
            if not self.clear_tables():
                return False

            # Step 5
            if not self.load_customers():
                return False
            
            # Step 6
            if not self.load_products():
                return False
            
            # Step 7
            if not self.load_orders():
                return False
            
            # Step 8
            if not self.load_order_items():
                return False
            
            # Step 9
            if not self.load_transactions():
                return False
            
            # Step 10
            if not self.validate_data():
                return False
            
            logger.info("=" * 50)
            logger.info("ETL Pipeline completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"ETL Pipeline failed: {e}")
            return False
        
        finally:
            if self.conn:
                self.conn.close()
                logger.info("Database connection closed")

def main():
    """Main function to run ETL"""
    etl = RobustETL()
    success = etl.run_etl()
    
    if success:
        print("\nETL process completed successfully!")
        print(" Data has been loaded into your PostgreSQL database.")
        print("You can now view the data in pgAdmin or run queries.")
    else:
        print("ETL process failed. Check the logs above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()