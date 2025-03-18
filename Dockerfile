FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p data

# Set environment variables
ENV AIRBNB_DATA_DIR=/app/data
ENV AIRBNB_INPUT_FILE=airbnb91.csv
ENV LOG_LEVEL=INFO

# Expose the port Dagster runs on
EXPOSE 3000

# Start Dagster
CMD ["dagster", "dev", "-f", "sales_pipeline/assets.py", "--host", "0.0.0.0"] 