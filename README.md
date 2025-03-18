# Airbnb Financial Analysis Pipeline

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables in `.env`
3. Start pipeline: `dagster dev`

## Configuration
- Set environment variables in `.env`:
  - AIRBNB_DATA_DIR: Directory for data files
  - AIRBNB_INPUT_FILE: Input CSV filename
  - LOG_LEVEL: Logging level (INFO/DEBUG/ERROR) 