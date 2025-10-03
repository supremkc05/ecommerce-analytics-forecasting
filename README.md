# 🛍️ E-commerce Analytics & Forecasting Pipeline

A production-ready **data engineering and analytics platform** that processes 358,277+ e-commerce transactions to deliver actionable business insights through automated ETL pipelines, comprehensive analytics, and Docker containerization.

## 🎯 Project Overview

This project demonstrates enterprise-level data engineering practices with:
- **Scalable ETL Pipeline**: Processes 358K+ transactions with batch processing and error handling
- **Business Intelligence**: Customer segmentation, revenue analytics, and geographic insights
- **Production Architecture**: Professional file hierarchy, Docker containerization, and modular design
- **Data Quality**: Foreign key constraints, referential integrity, and comprehensive validation

## 📊 Key Metrics & Results

### Database Performance
- **📈 358,277 transactions** processed successfully
- **👥 4,314 unique customers** with complete profiles
- **🏷️ 2,785 products** with pricing and inventory data
- **📦 18,220 orders** with geographic distribution
- **💰 £7,993,225** total revenue processed

### Business Insights Generated
- **🏆 Top Customer**: £265,106 spending (Customer 14646)
- **🌍 Primary Market**: UK (£6.6M revenue, 318K transactions)
- **📈 Peak Period**: November 2011 (£1.05M revenue)
- **👑 VIP Customers**: 232 customers generating £4.1M revenue

## 🏗️ Architecture & Structure

```
📁 ecommerce-analytics-forecasting/
├── 📁 src/                          # Main source code
│   ├── 📁 etl/
│   │   ├── robust_etl.py           # Production ETL pipeline
│   │   └── __init__.py
│   ├── 📁 database/
│   │   ├── config.py               # Database configuration
│   │   ├── database.py             # Connection utilities
│   │   └── __init__.py
│   ├── 📁 analysis/
│   │   ├── analyze_data.py         # Business intelligence queries
│   │   ├── final_status.py         # ETL validation & reporting
│   │   └── __init__.py
│   └── __init__.py
├── 📁 scripts/
│   ├── run_etl.py                  # ETL runner script
│   └── run_analysis.py             # Analysis runner
├── 📁 notebooks/
│   └── etl_pipeline.ipynb          # Interactive analysis
├── 📁 docs/
│   └── ETL_README.md               # Technical documentation
├── 📁 docker/
│   ├── Dockerfile                  # Container definition
│   ├── docker-compose.yml          # Multi-container setup
│   └── init.sql                    # Database schema
├── 📁 data/
│   ├── data.csv                    # Raw dataset
│   └── cleaned_data.csv            # Processed data
├── .env                            # Environment variables
├── requirements.txt                # Dependencies
└── README.md                       # This file
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.13+**
- **PostgreSQL 17+** 
- **Docker** (optional for containerization)

### Option 1: Local Setup

```bash
# 1. Clone and setup
git clone https://github.com/supremkc05/ecommerce-analytics-forecasting.git
cd ecommerce-analytics-forecasting

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 3. Configure environment
# Update .env file with your database credentials:
DB_HOST=localhost
DB_NAME=ecommerce_analytics
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432

# 4. Run ETL Pipeline
python scripts/run_etl.py

# 5. Generate Analytics
python scripts/run_analysis.py
```

### Option 2: Docker Setup

```bash
# 1. Build and start containers
cd docker
docker-compose up --build -d

# 2. Access services
# - Database: localhost:5432
# - pgAdmin: http://localhost:8080 (admin@example.com / admin123)

# 3. Check logs
docker-compose logs -f etl_app
```

## 📈 Analytics & Insights

### Customer Segmentation
- **🏆 VIP Customers**: 232 customers (£17,747 avg spend)
- **⭐ Premium**: 1,298 customers (£2,131 avg spend)  
- **👤 Regular**: 2,550 customers (£429 avg spend)
- **🔰 Basic**: 234 customers (£68 avg spend)

### Geographic Distribution 
- **🇬🇧 United Kingdom**: £6.6M (82.6% of revenue)
- **🇳🇱 Netherlands**: £269K (3.4% of revenue)
- **🇮🇪 Ireland**: £242K (3.0% of revenue)
- **🇩🇪 Germany**: £190K (2.4% of revenue)

### Product Performance
- **🎨 Paper Craft Little Birdie**: £168K revenue
- **🍰 Regency Cakestand 3 Tier**: £142K revenue  
- **🏺 Medium Ceramic Storage Jar**: £81K revenue

## 🛠️ Technical Features

### ETL Pipeline
- ✅ **Batch Processing**: Handles 358K+ records efficiently
- ✅ **Data Validation**: Foreign key constraints and referential integrity
- ✅ **Error Handling**: Comprehensive logging and rollback mechanisms
- ✅ **Performance**: Optimized with batch commits and indexing

### Database Design
- ✅ **Normalized Schema**: 5 tables with proper relationships
- ✅ **Performance Indexes**: Optimized for analytics queries
- ✅ **Data Types**: Proper numeric precision for financial data
- ✅ **Constraints**: CASCADE deletes and data validation

### Analytics Engine
- ✅ **Business Intelligence**: 6+ analytical queries
- ✅ **Time Series**: Monthly trend analysis
- ✅ **Customer Analytics**: RFM-style segmentation
- ✅ **Geographic Analysis**: Country-level revenue breakdown

## 🐳 Docker Containerization

### Services
- **PostgreSQL 17.6**: Database with auto-initialization
- **ETL Application**: Python-based processing engine
- **pgAdmin**: Web-based database management
- **Health Checks**: Automated service monitoring

### Commands
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f etl_app

# Stop services
docker-compose down

# Clean reset
docker-compose down -v
```

## 📋 Usage Examples

### Running ETL Pipeline
```bash
# Full pipeline execution
python scripts/run_etl.py

# Output:
# 🚀 Starting Ecommerce Analytics ETL Pipeline...
# ✅ Connected to PostgreSQL database successfully
# ✅ Extracted 358,277 rows from data/cleaned_data.csv
# ✅ Data transformation completed
# ✅ Successfully loaded 4,314 customers
# ✅ Successfully loaded 2,785 products
# ✅ ETL Pipeline completed successfully!
```

### Generating Business Reports
```bash
# Comprehensive analytics
python scripts/run_analysis.py

# Output includes:
# - Database status validation
# - Top customers and products
# - Geographic revenue analysis  
# - Monthly sales trends
# - Customer segmentation
```

## 🎯 Business Value

### For Data Engineers
- **Scalable Architecture**: Handles large datasets with batch processing
- **Production Ready**: Error handling, logging, and monitoring
- **Modern Stack**: Python 3.13, PostgreSQL 17, Docker containerization

### For Business Analysts
- **Customer Insights**: Identify high-value customers and segments
- **Revenue Analytics**: Track performance across time and geography
- **Operational Metrics**: Monitor order values and transaction patterns

### For Decision Makers
- **Revenue Optimization**: Focus on £17K+ VIP customer segment
- **Market Expansion**: Leverage UK success for international growth
- **Product Strategy**: Prioritize high-performing product categories

## 🔧 Development

### Testing
```bash
# Test database connection
python src/database/database.py

# Validate ETL components
python src/etl/robust_etl.py

# Check analysis queries
python src/analysis/final_status.py
```

### Monitoring
- **Health Checks**: Docker container monitoring
- **Data Validation**: Automated ETL success verification
- **Performance Metrics**: Query execution times and throughput

## 🚀 Future Enhancements

- [ ] **Machine Learning**: Demand forecasting and customer lifetime value
- [ ] **Real-time Processing**: Streaming ETL with Apache Kafka
- [ ] **Visualization**: Grafana dashboards and Power BI integration
- [ ] **API Layer**: REST API for analytics consumption
- [ ] **Data Warehouse**: Dimensional modeling with fact/dimension tables

## � Contact

**Suprem KC**
- GitHub: [@supremkc05](https://github.com/supremkc05)
- Project: [ecommerce-analytics-forecasting](https://github.com/supremkc05/ecommerce-analytics-forecasting)

---

**🎯 This project demonstrates production-level data engineering skills with real business impact: processing 358K+ transactions to generate £7.9M in analyzed revenue with actionable customer and product insights.**
