FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create data directory if it doesn't exist
RUN mkdir -p /app/data

# Set proper permissions
RUN chmod +x *.py

# Create non-root user for security
RUN groupadd -r etluser && useradd -r -g etluser etluser
RUN chown -R etluser:etluser /app
USER etluser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import psycopg2; print('Health check passed')" || exit 1

# Default command - run the ETL pipeline
CMD ["python", "scripts/run_etl.py"]
