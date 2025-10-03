
-- Initialize ecommerce analytics database schema
-- This script will be run when the PostgreSQL container starts

-- Create customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    first_purchase_date DATE,
    last_purchase_date DATE,
    total_spent NUMERIC(10,2),
    total_orders INTEGER,
    avg_order_value NUMERIC(10,2)
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    stock_code VARCHAR(50) PRIMARY KEY,
    description TEXT,
    unit_price NUMERIC(10,2),
    first_seen_date DATE
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    invoice_no VARCHAR(50) PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id) ON DELETE CASCADE,
    invoice_date TIMESTAMP,
    country VARCHAR(100),
    total_amount NUMERIC(10,2),
    total_items INTEGER
);

-- Create order_items table
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    invoice_no VARCHAR(50) REFERENCES orders(invoice_no) ON DELETE CASCADE,
    stock_code VARCHAR(50) REFERENCES products(stock_code) ON DELETE CASCADE,
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    total_price NUMERIC(10,2)
);

-- Create transactions table (complete transaction log)
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    invoice_no VARCHAR(50),
    stock_code VARCHAR(50),
    customer_id INTEGER,
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    total_price NUMERIC(10,2),
    invoice_date TIMESTAMP,
    country VARCHAR(100)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_customers_total_spent ON customers(total_spent DESC);
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(invoice_date);
CREATE INDEX IF NOT EXISTS idx_order_items_invoice ON order_items(invoice_no);
CREATE INDEX IF NOT EXISTS idx_transactions_customer ON transactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(invoice_date);
CREATE INDEX IF NOT EXISTS idx_transactions_country ON transactions(country);

-- Grant permissions on individual tables
GRANT ALL PRIVILEGES ON customers TO postgres;
GRANT ALL PRIVILEGES ON products TO postgres;
GRANT ALL PRIVILEGES ON orders TO postgres;
GRANT ALL PRIVILEGES ON order_items TO postgres;
GRANT ALL PRIVILEGES ON transactions TO postgres;

-- Grant permissions on sequences
GRANT ALL PRIVILEGES ON order_items_id_seq TO postgres;
GRANT ALL PRIVILEGES ON transactions_id_seq TO postgres;