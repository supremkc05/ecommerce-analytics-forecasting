import psycopg2
import sys
from pathlib import Path

# Add database module to path
sys.path.append(str(Path(__file__).parent.parent / "database"))
from config import DB_CONFIG

def final_status():
    """Show final ETL status and sample data"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("FINAL ETL STATUS REPORT")
        print("=" * 50)
        
        # Get table counts
        tables = ['customers', 'products', 'orders', 'order_items', 'transactions']
        table_counts = {}
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            table_counts[table] = count
            
            status = "Pass" if count > 0 else "fail"
            print(f"{status} {table}: {count:,} records")
        
        print("\nDATA SUMMARY")
        print("=" * 50)
        
        if table_counts['customers'] > 0:
            # Top customers
            cursor.execute("""
                SELECT customer_id, total_spent, total_orders 
                FROM customers 
                ORDER BY total_spent DESC 
                LIMIT 3
            """)
            top_customers = cursor.fetchall()
            print("\nTop 3 Customers by Spending:")
            for i, (customer_id, spent, orders) in enumerate(top_customers, 1):
                print(f"   {i}. Customer {customer_id}: £{spent:.2f} ({orders} orders)")
        
        if table_counts['products'] > 0:
            # Most expensive products
            cursor.execute("""
                SELECT stock_code, description, unit_price 
                FROM products 
                ORDER BY unit_price DESC 
                LIMIT 3
            """)
            top_products = cursor.fetchall()
            print("\nTop 3 Most Expensive Products:")
            for i, (code, desc, price) in enumerate(top_products, 1):
                desc_short = desc[:40] + "..." if len(desc) > 40 else desc
                print(f"   {i}. {code}: {desc_short} - £{price:.2f}")
        
        if table_counts['orders'] > 0:
            # Order summary
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_orders,
                    ROUND(AVG(total_amount), 2) as avg_order_value,
                    ROUND(SUM(total_amount), 2) as total_revenue
                FROM orders
            """)
            order_stats = cursor.fetchone()
            print(f"\nOrder Statistics:")
            print(f"   Total Orders: {order_stats[0]:,}")
            print(f"   Average Order Value: £{order_stats[1]:.2f}")
            print(f"   Total Revenue: £{order_stats[2]:,.2f}")
        
        if table_counts['transactions'] > 0:
            # Transaction summary by country
            cursor.execute("""
                SELECT country, COUNT(*) as transactions, ROUND(SUM(total_price), 2) as revenue
                FROM transactions 
                GROUP BY country 
                ORDER BY revenue DESC 
                LIMIT 5
            """)
            country_stats = cursor.fetchall()
            print(f"\nTop 5 Countries by Revenue:")
            for i, (country, trans, revenue) in enumerate(country_stats, 1):
                print(f"   {i}. {country}: {trans:,} transactions, £{revenue:,.2f}")
        
        print("\n" + "=" * 50)
        
        # Check completion status
        expected_counts = {
            'customers': 4314,
            'products': 2785,
            'orders': 9200,
            'order_items': 358277,
            'transactions': 358277
        }
        
        all_complete = True
        for table, expected in expected_counts.items():
            actual = table_counts[table]
            if actual == 0:
                all_complete = False
                print(f"{table} is empty (expected {expected:,})")
            elif actual < expected * 0.9:  # Allow some variance
                print(f"{table} partially loaded: {actual:,} / {expected:,}")
        
        if all_complete and all(count > 0 for count in table_counts.values()):
            print("ETL COMPLETED SUCCESSFULLY!")
            print("All tables are populated with data")
            print("\nNext Steps:")
            print("   1. Open pgAdmin to explore the data visually")
            print("   2. Connect to database: localhost:5432/ecommerce_analytics")
            print("   3. Navigate to: Schemas → public → Tables")
            print("   4. Right-click any table → View/Edit Data → All Rows")
        else:
            incomplete_tables = [table for table, count in table_counts.items() if count == 0]
            if incomplete_tables:
                print(f"Still loading: {', '.join(incomplete_tables)}")
                print("Check again in a few minutes...")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error checking status: {e}")

if __name__ == "__main__":
    final_status()