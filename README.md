# Ecommerce Analytics & Forecasting

A complete ETL pipeline that transforms ecommerce transaction data into actionable business insights. Perfect for analyzing customer behavior, sales trends, and business performance.

## Quick Start

### Prerequisites
- Docker & Docker Compose installed
- Git (optional, for cloning)
- 4GB+ RAM available for Docker

### Getting Started

1. **Clone or Download**
   ```bash
   git clone https://github.com/supremkc05/ecommerce-analytics-forecasting.git
   cd ecommerce-analytics-forecasting
   ```

2. **Add Your Data**
   - Place your CSV file in the `data/` directory
   - Name it `cleaned_data.csv` (or update the config)

3. **Run Everything**
   ```bash
   # Start all services
   docker-compose up --build -d

   # Watch the ETL process
   docker-compose logs -f etl_app

   # Access database admin at http://localhost:8080
   # Username: admin@example.com #use your own
   # Password: admin123
   ```

That's it! Your data is now processed and ready for analysis.

##  What You'll Get

After running the pipeline, you'll see outputs like:

### ETL Pipeline Results
```
Starting Ecommerce Analytics ETL Pipeline...
Connected to PostgreSQL database successfully
Extracted 358,277 rows from data/cleaned_data.csv
Data transformation completed
Successfully loaded 4,314 customers
Successfully loaded 2,785 products
ETL Pipeline completed successfully!
```

### Business Analytics
- **Customer Segmentation**: VIP, Premium, Regular, and Basic customer tiers
- **Top Performers**: Highest spending customers and best-selling products
- **Geographic Analysis**: Revenue breakdown by country
- **Time Trends**: Monthly sales patterns and seasonal insights

## Analytics Overview

### Customer Segmentation
- **VIP (5.4%)**: 232 customers, £17K+ avg spend - Drive 52% of revenue
- **Premium (30%)**: 1,298 customers, £2K avg spend - Growth potential  
- **Regular (59%)**: 2,550 customers, £429 avg spend - Volume base
- **Basic (5.4%)**: 234 customers, £68 avg spend - New buyers

### Geographic Distribution
- **🇬🇧 UK**: £6.6M (82.6%) - Dominant market
- **🇳🇱 Netherlands**: £269K (3.4%) - Growth opportunity
- **🇮🇪 Ireland**: £242K (3.0%) - Stable market
- **🇩🇪 Germany**: £190K (2.4%) - Expansion potential

### Top Products
1. **Paper Craft Little Birdie**: £168K revenue
2. **Regency Cakestand 3 Tier**: £142K revenue  
3. **Medium Ceramic Storage Jar**: £81K revenue

### Key Metrics
- **Total Revenue**: £7.9M across 358K+ transactions
- **Average Order**: £22.45 per transaction
- **Peak Season**: November-December (holiday surge)
- **Product Range**: 2,785 unique items

## Project Structure

```
ecommerce-analytics-forecasting/
├── scripts/
│   ├── run_etl.py              # Main ETL runner
│   └── run_analysis.py         # Analytics generator
├── src/
│   ├── etl/                    # ETL logic
│   ├── database/               # Database settings
│   └── analysis/               # Analytics queries
├── docker/
│   ├── docker-compose.yml      # Container setup
│   └── Dockerfile              # Application container
├── data/
│   └── cleaned_data.csv        # Your source data
└── .env                        # Database configuration
```

## Usage Examples

### Running ETL Pipeline
```bash
# Full pipeline execution
python scripts/run_etl.py

# Output shows successful data loading
```

### Generating Business Reports
```bash
# Run analytics to see insights
python scripts/run_analysis.py

# You'll see reports on:
# - Top customers and products
# - Sales by country and month
# - Customer segmentation analysis
```

## Need Help?

### Common Issues

**Database Connection Failed**
```bash
# Check if PostgreSQL is running
docker-compose ps

# View database logs  
docker-compose logs postgres
```

**ETL Pipeline Errors**
```bash
# Check application logs
docker-compose logs etl_app

# Run manually for debugging
python scripts/run_etl.py
```

**Port 5432 Already in Use**
```bash
# Stop existing PostgreSQL services
taskkill /F /IM postgres.exe

# Or change port in docker-compose.yml
```

