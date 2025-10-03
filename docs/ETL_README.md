# Simple ETL Pipeline Guide

This guide explains how to run the ETL (Extract, Transform, Load) process for your e-commerce data.

## 📋 Overview

The ETL process consists of:
1. **Extract**: Read data from CSV file (`data/cleaned_data.csv`)
2. **Transform**: Clean and prepare data for analysis
3. **Load**: Insert data into PostgreSQL database

## 🚀 How to Run ETL

### Step 1: Activate Virtual Environment
```powershell
venv\Scripts\Activate.ps1
```

### Step 2: Run ETL Pipeline
```powershell
python simple_etl.py
```

### Step 3: Analyze Data (Optional)
```powershell
python analyze_data.py
```

## 📊 What the ETL Creates

The process creates 3 tables in your PostgreSQL database:

### 1. `customers` table
- `customer_id`: Unique customer identifier
- `country`: Customer's country
- `first_purchase`: Date of first purchase
- `last_purchase`: Date of last purchase
- `total_spent`: Total amount spent by customer
- `total_orders`: Number of orders placed

### 2. `products` table
- `stock_code`: Unique product identifier
- `description`: Product description
- `avg_price`: Average selling price
- `total_quantity_sold`: Total units sold
- `total_revenue`: Total revenue from product

### 3. `transactions` table
- `id`: Auto-generated transaction ID
- `invoice_no`: Invoice number
- `stock_code`: Product code (links to products table)
- `customer_id`: Customer ID (links to customers table)
- `quantity`: Number of items purchased
- `unit_price`: Price per unit
- `total_price`: Total transaction value
- `invoice_date`: Date of transaction
- `country`: Country where transaction occurred

## 🔍 Sample Queries

After running the ETL, you can query your data:

```sql
-- Top 10 customers by spending
SELECT customer_id, country, total_spent 
FROM customers 
ORDER BY total_spent DESC 
LIMIT 10;

-- Monthly sales summary
SELECT 
    DATE_TRUNC('month', invoice_date) as month,
    COUNT(*) as transactions,
    SUM(total_price) as revenue
FROM transactions
GROUP BY month
ORDER BY month;

-- Product performance
SELECT 
    stock_code, 
    description, 
    total_revenue, 
    total_quantity_sold
FROM products
ORDER BY total_revenue DESC
LIMIT 10;
```

## 🛠️ Troubleshooting

### Common Issues:

1. **Database Connection Error**
   - Check your `.env` file has correct database credentials
   - Ensure PostgreSQL is running

2. **File Not Found Error**
   - Verify `data/cleaned_data.csv` exists
   - Check file path in `config.py`

3. **Permission Error**
   - Make sure you have write permissions to the database
   - Check if virtual environment is activated

### Getting Help:

1. Check the console output for detailed error messages
2. Look at the log messages (they use emojis to show progress!)
3. Verify your database connection settings in `.env`

## 📈 What's Next?

After successful ETL, you can:
1. Run the analysis script to see data insights
2. Connect to your database with tools like pgAdmin or DBeaver
3. Create dashboards using tools like Tableau or Power BI
4. Build APIs to serve the data to applications

## 🔧 Files in this ETL

- `simple_etl.py`: Main ETL pipeline script
- `analyze_data.py`: Data analysis and sample queries
- `config.py`: Configuration settings
- `.env`: Database credentials (keep private!)
- `data/cleaned_data.csv`: Source data file

Happy analyzing! 🎉