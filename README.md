# E-commerce Sales Analytics & Demand Forecasting

An end-to-end data engineering + analytics + machine learning project that demonstrates how to collect, clean, analyze, and forecast e-commerce sales data.

This project integrates ETL pipelines, interactive dashboards, and time-series forecasting models to showcase skills across data engineering, analytics, and AI/ML.

## Project Overview

This project follows a **step-by-step learning approach** to build a professional-grade analytics pipeline:

- **Data Engineering**: ETL pipelines with PostgreSQL database
- **Data Analytics**: RFM analysis, customer segmentation, and business insights
- **Machine Learning**: Time-series forecasting for demand prediction
- **Visualization**: Interactive dashboards and reporting

## Project Structure

```
ecommerce-analytics-forcasting/
├── config.py              # Configuration management with environment variables
├── database.py             # PostgreSQL connection and utilities
├── etl_pipeline.ipynb      # Jupyter notebook with data analysis and ETL
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (not in git)
├── data/
│   └── data.csv           # Raw e-commerce dataset
|   └── cleaned_data.csv 
└── README.md              # This file
```

## Progress Tracker

### ✅ Completed Steps

1. **Data Exploration & Cleaning** *(etl_pipeline.ipynb)*
   - Data quality assessment and cleaning
   - Removed cancelled orders and invalid records
   - Handled missing values and duplicates
   - Created calculated fields (TotalPrice)

2. **Customer Analytics** *(etl_pipeline.ipynb)*
   - RFM Analysis (Recency, Frequency, Monetary)
   - Revenue trends and customer segmentation
   - Top customer identification
   - Monthly revenue analysis

3. **Configuration Management** *(config.py)*
   - Environment variable management
   - Secure database configuration
   - Validation functions

4. **Database Infrastructure** *(database.py)*
   - PostgreSQL connection management
   - Database testing utilities
   - Error handling

5. **Database Schema Design** *(etl_pipeline.ipynb)*
   - Normalized database schema (customers, products, orders, order_items)
   - Performance indexes and constraints
   - Business intelligence views
   - Automated triggers for data consistency


## Getting Started

### Prerequisites
- Python 3.13+
- PostgreSQL 17+
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/supremkc05/ecommerce-analytics-forecasting.git
   cd ecommerce-analytics-forecasting
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update database credentials:
   ```
   DB_HOST=localhost
   DB_NAME=ecommerce_analytics
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_PORT=5432
   ```

4. **Test configuration**
   ```bash
   python config.py
   python database.py
   ```

5. **Run the Jupyter notebook**
   ```bash
   jupyter notebook etl_pipeline.ipynb
   ```

## Business Value

This project demonstrates:
- **Data Engineering** best practices with modular, scalable code
- **Analytics** capabilities for business decision making
- **Machine Learning** applications for predictive insights
- **Database Design** for enterprise-grade data storage

## Learning Outcomes

Through this step-by-step approach, you'll master:
- ETL pipeline development
- Database schema design and optimization  
- Customer analytics and segmentation
- Time-series forecasting techniques
- Professional project structure and documentation

## 📧 Contact

**Suprem KC** - [GitHub](https://github.com/supremkc05)

---
*This project is part of a data engineering and analytics learning journey. Each step builds upon the previous one to create a comprehensive, production-ready system.*
