import psycopg2
import pandas as pd
from urllib.parse import quote_plus
import logging
import sys
from pathlib import Path

# Add parent path
sys.path.append(str(Path(__file__).parent.parent / "database"))
from config import DB_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataAnalyzer:
    def __init__(self):
        self.conn = None
        
    def connect(self):
        """Connect to database"""
        try:
            self.conn = psycopg2.connect(
                host=DB_CONFIG['host'],
                database=DB_CONFIG['database'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                port=DB_CONFIG['port']
            )
            logger.info("Connected to database")
            return True
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False
    
    def run_query(self, query, description):
        """Run a query and display results"""
        try:
            print(f"\n{description}")
            print("=" * 60)
            
            df = pd.read_sql_query(query, self.conn)
            print(df.to_string(index=False))
            print(f"\nQuery returned {len(df)} rows")
            
        except Exception as e:
            print(f"Query failed: {e}")
    
    def analyze_data(self):
        """Run various analysis queries"""
        
        # 1. Basic statistics
        self.run_query("""
            SELECT 
                COUNT(*) as total_transactions,
                COUNT(DISTINCT customer_id) as unique_customers,
                COUNT(DISTINCT stock_code) as unique_products,
                ROUND(AVG(total_price), 2) as avg_transaction_value,
                ROUND(SUM(total_price), 2) as total_revenue
            FROM transactions
        """, "Basic Statistics")
        
        # 2. Top 10 customers by spending
        self.run_query("""
            SELECT 
                customer_id,
                total_spent,
                total_orders,
                ROUND(total_spent / total_orders, 2) as avg_order_value
            FROM customers
            ORDER BY total_spent DESC
            LIMIT 10
        """, "Top 10 Customers by Total Spending")
        
        # 3. Top 10 products by revenue (calculated from transactions)
        self.run_query("""
            SELECT 
                p.stock_code,
                p.description,
                p.unit_price,
                COUNT(t.stock_code) as times_sold,
                ROUND(SUM(t.total_price), 2) as total_revenue
            FROM products p
            LEFT JOIN transactions t ON p.stock_code = t.stock_code
            GROUP BY p.stock_code, p.description, p.unit_price
            ORDER BY total_revenue DESC
            LIMIT 10
        """, "Top 10 Products by Revenue")
        
        # 4. Sales by country
        self.run_query("""
            SELECT 
                country,
                COUNT(*) as total_transactions,
                COUNT(DISTINCT customer_id) as unique_customers,
                ROUND(SUM(total_price), 2) as total_revenue
            FROM transactions
            GROUP BY country
            ORDER BY total_revenue DESC
            LIMIT 10
        """, "Sales by Country (Top 10)")
        
        # 5. Monthly sales trend
        self.run_query("""
            SELECT 
                DATE_TRUNC('month', invoice_date) as month,
                COUNT(*) as transactions,
                COUNT(DISTINCT customer_id) as customers,
                ROUND(SUM(total_price), 2) as revenue
            FROM transactions
            GROUP BY DATE_TRUNC('month', invoice_date)
            ORDER BY month
        """, "Monthly Sales Trend")
        
        # 6. Customer segmentation
        self.run_query("""
            SELECT 
                CASE 
                    WHEN total_spent >= 5000 THEN 'VIP'
                    WHEN total_spent >= 1000 THEN 'Premium'
                    WHEN total_spent >= 100 THEN 'Regular'
                    ELSE 'Basic'
                END as customer_segment,
                COUNT(*) as customer_count,
                ROUND(AVG(total_spent), 2) as avg_spending,
                ROUND(SUM(total_spent), 2) as segment_revenue
            FROM customers
            GROUP BY CASE 
                    WHEN total_spent >= 5000 THEN 'VIP'
                    WHEN total_spent >= 1000 THEN 'Premium'
                    WHEN total_spent >= 100 THEN 'Regular'
                    ELSE 'Basic'
                END
            ORDER BY avg_spending DESC
        """, "Customer Segmentation")

def main():
    """Main function"""
    analyzer = DataAnalyzer()
    
    if analyzer.connect():
        print("Starting Data Analysis...")
        analyzer.analyze_data()
        print("\nAnalysis completed!")
        
        if analyzer.conn:
            analyzer.conn.close()
    else:
        print("Failed to connect to database")

if __name__ == "__main__":
    main()