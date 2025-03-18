import pandas as pd
from dagster import asset, Definitions, MetadataValue, Output
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asset
def raw_airbnb_data():
    """
    Extract: Read Airbnb financial data from CSV
    """
    try:
        file_path = 'data/airbnb91.csv'
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")
            
        df = pd.read_csv(file_path, parse_dates=['Month'])
        
        # Add data quality checks
        if df.empty:
            raise ValueError("Empty dataset loaded")
            
        required_columns = ['Month', 'Items', 'Cost', 'Transaction Type']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
            
        logger.info(f"Successfully loaded {len(df)} records")
        
        return Output(
            df,
            metadata={
                "row_count": MetadataValue.int(len(df)),
                "preview": MetadataValue.md(df.head().to_markdown())
            }
        )
        
    except Exception as e:
        logger.error(f"Error loading raw data: {str(e)}")
        raise

@asset
def monthly_revenue_analysis(raw_airbnb_data):
    """
    Transform: Calculate monthly revenue metrics including:
    - Total Income by platform (Airbnb, VRBO, Cash)
    - Total Expenses by category
    - Net Profit
    """
    # Group income by platform and month
    income_by_platform = raw_airbnb_data[raw_airbnb_data['Transaction Type'] == 'Income'] \
        .groupby(['Month', 'Items'])['Cost'].sum() \
        .reset_index()
    
    # Group expenses by category and month
    expenses_by_category = raw_airbnb_data[raw_airbnb_data['Transaction Type'] == 'Expense'] \
        .groupby(['Month', 'Items'])['Cost'].sum() \
        .reset_index()
    
    # Calculate monthly totals
    monthly_summary = raw_airbnb_data.groupby('Month').agg({
        'Total Income': 'sum',
        'Total Expense': 'sum',
        'Total Cleaning for All Time': 'sum',
        'Net Profit': 'sum'
    }).reset_index()
    
    return {
        'income_by_platform': income_by_platform,
        'expenses_by_category': expenses_by_category,
        'monthly_summary': monthly_summary
    }

@asset
def financial_metrics(monthly_revenue_analysis):
    """
    Transform: Calculate key financial metrics and KPIs
    """
    monthly_summary = monthly_revenue_analysis['monthly_summary']
    
    metrics = {
        'total_revenue': monthly_summary['Total Income'].sum(),
        'total_expenses': monthly_summary['Total Expense'].sum(),
        'total_cleaning': monthly_summary['Total Cleaning for All Time'].sum(),
        'total_net_profit': monthly_summary['Net Profit'].sum(),
        'average_monthly_profit': monthly_summary['Net Profit'].mean(),
        'profit_margin': (monthly_summary['Net Profit'].sum() / monthly_summary['Total Income'].sum()) * 100
    }
    
    return pd.DataFrame([metrics])

@asset
def store_analysis_results(monthly_revenue_analysis, financial_metrics):
    """
    Load: Store all analysis results to CSV files
    """
    # Save detailed monthly analyses
    monthly_revenue_analysis['income_by_platform'].to_csv('data/income_by_platform.csv', index=False)
    monthly_revenue_analysis['expenses_by_category'].to_csv('data/expenses_by_category.csv', index=False)
    monthly_revenue_analysis['monthly_summary'].to_csv('data/monthly_summary.csv', index=False)
    
    # Save overall financial metrics
    financial_metrics.to_csv('data/financial_metrics.csv', index=False)

    # return the financial metrics
    return {
        'financial_metrics': financial_metrics,
        'monthly_revenue': monthly_revenue_analysis
    }

defs = Definitions(
    assets=[raw_airbnb_data, monthly_revenue_analysis, financial_metrics, store_analysis_results]
)