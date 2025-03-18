import os
from pathlib import Path

class Settings:
    DATA_DIR = os.getenv('AIRBNB_DATA_DIR', 'data')
    INPUT_FILE = os.getenv('AIRBNB_INPUT_FILE', 'airbnb91.csv')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO') 