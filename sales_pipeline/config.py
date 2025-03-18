from dagster import Config
from dataclasses import dataclass

@dataclass
class AirbnbPipelineConfig(Config):
    input_file_path: str = "data/airbnb91.csv"
    output_directory: str = "data"
    date_column: str = "Month" 