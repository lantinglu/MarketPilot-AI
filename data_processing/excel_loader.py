"""Load all sheets from Excel workbooks into pandas DataFrames."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_excel_workbook(path: str | Path) -> dict[str, pd.DataFrame]:
    """Read every sheet in an Excel workbook."""

    workbook_path = Path(path)
    excel = pd.ExcelFile(workbook_path)
    sheets = {}
    for sheet_name in excel.sheet_names:
        df = pd.read_excel(workbook_path, sheet_name=sheet_name)
        if not df.empty:
            sheets[sheet_name] = df
    return sheets


def load_excel_directory(raw_dir: str | Path) -> dict[str, pd.DataFrame]:
    """Read all .xlsx/.xls files in a directory and namespace sheets by file."""

    raw_path = Path(raw_dir)
    loaded = {}
    for workbook_path in sorted(raw_path.glob("*.xls*")):
        for sheet_name, df in load_excel_workbook(workbook_path).items():
            loaded[f"{workbook_path.name}::{sheet_name}"] = df
    return loaded

