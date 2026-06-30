"""Project configuration for Market Entry Agent."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_DATA_DIR = DATA_DIR / "sample"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

STANDARD_DATASET_CSV = PROCESSED_DATA_DIR / "market_entry_dataset.csv"
STANDARD_DATASET_JSON = PROCESSED_DATA_DIR / "market_entry_dataset.json"
STANDARD_DATASET_SQLITE = PROCESSED_DATA_DIR / "market_entry_dataset.sqlite"
SAMPLE_DATASET_CSV = SAMPLE_DATA_DIR / "sample_market_entry_dataset.csv"

