"""Build the standardized data layer from raw Excel files plus sample data."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from config import RAW_DATA_DIR, PROCESSED_DATA_DIR, SAMPLE_DATASET_CSV, STANDARD_DATASET_CSV, STANDARD_DATASET_JSON, STANDARD_DATASET_SQLITE
from data_processing.data_cleaner import combine_and_clean
from data_processing.data_schema import STANDARD_COLUMNS, sample_records
from data_processing.excel_loader import load_excel_directory


def build_dataset() -> pd.DataFrame:
    """Create CSV, JSON, and SQLite outputs for the Retriever Agent."""

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    SAMPLE_DATASET_CSV.parent.mkdir(parents=True, exist_ok=True)

    sample_df = pd.DataFrame(sample_records(), columns=STANDARD_COLUMNS)
    sample_df.to_csv(SAMPLE_DATASET_CSV, index=False)

    sheets = load_excel_directory(RAW_DATA_DIR)
    excel_df = combine_and_clean(sheets) if sheets else pd.DataFrame(columns=STANDARD_COLUMNS)
    combined = pd.concat([excel_df, sample_df], ignore_index=True)
    combined = combined[STANDARD_COLUMNS].drop_duplicates()

    combined.to_csv(STANDARD_DATASET_CSV, index=False)
    combined.to_json(STANDARD_DATASET_JSON, orient="records", indent=2, force_ascii=False)

    with sqlite3.connect(STANDARD_DATASET_SQLITE) as conn:
        combined.to_sql("market_entry_data", conn, if_exists="replace", index=False)

    return combined


if __name__ == "__main__":
    dataset = build_dataset()
    source_count = (dataset["source_type"] == "platform_data_source").sum()
    sample_count = (dataset["source_type"] == "sample_estimate").sum()
    print("Dataset build complete")
    print(f"Rows: {len(dataset)}")
    print(f"Excel-derived platform/source rows: {source_count}")
    print(f"Sample fallback metric rows: {sample_count}")
    print(f"CSV: {STANDARD_DATASET_CSV}")
    print(f"JSON: {STANDARD_DATASET_JSON}")
    print(f"SQLite: {STANDARD_DATASET_SQLITE}")

