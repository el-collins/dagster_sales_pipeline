# Airbnb Sales Pipeline

A Dagster pipeline for processing Airbnb financial data.

## Project Structure
```
sales_pipeline/
├── __init__.py
└── assets.py      # Dagster ETL pipeline assets
```

## Setup

1. Install the package in development mode:
```bash
python -m venv .venv
source .venv/bin/activate # on windows use .venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the Dagster development server:
```bash
dagster dev -f sales_pipeline/assets.py
```

## Data Pipeline Flow

The pipeline processes Airbnb financial data through these steps:

1. **Data Loading & Validation** (`raw_airbnb_data`):
   - Loads data from `data/airbnb91.csv`
   - Performs basic data validation:
     - Checks for empty dataset
     - Validates required columns exist
     - Verifies data structure

2. **Revenue Analysis** (`monthly_revenue_analysis`):
   - Calculates income by platform (Airbnb, VRBO, Cash)
   - Groups expenses by category
   - Generates monthly summaries

3. **Financial Metrics** (`financial_metrics`):
   - Calculates key financial metrics:
     - Total revenue
     - Total expenses
     - Total cleaning costs
     - Net profit
     - Average monthly profit
     - Profit margin

## Output Files

The pipeline generates four CSV files in the `data/` directory:
- `income_by_platform.csv`: Revenue breakdown by platform
- `expenses_by_category.csv`: Expenses categorized by type
- `monthly_summary.csv`: Monthly financial overview
- `financial_metrics.csv`: Overall financial KPIs

## Directory Structure

```
dagster_sales_pipeline/
├── data/                      # Data directory
│   ├── airbnb91.csv          # Input data
│   ├── income_by_platform.csv
│   ├── expenses_by_category.csv
│   ├── monthly_summary.csv
│   └── financial_metrics.csv
└── sales_pipeline/           # Pipeline code
    ├── __init__.py
    └── assets.py            # ETL pipeline assets
``` 