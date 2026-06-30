"""Clean raw Excel rows into the canonical market entry schema."""

from __future__ import annotations

import re
from typing import Iterable

import pandas as pd

from data_processing.data_schema import STANDARD_COLUMNS, today_iso


COLUMN_ALIASES = {
    "country": "country",
    "country_market": "country",
    "country__market": "country",
    "market": "country",
    "country_market_": "country",
    "industry": "industry",
    "category": "industry",
    "product": "product",
    "platform": "platform",
    "main_website_url": "source_url",
    "website": "source_url",
    "url": "source_url",
    "source_url": "source_url",
    "source_name": "source_name",
    "data_available": "data_available",
    "suitable_for": "suitable_for",
    "ranking_bestseller_url": "ranking_url",
    "search_url_example": "search_url_example",
    "updated_date": "updated_date",
    "notes": "notes",
}


def clean_sheet(df: pd.DataFrame, source_label: str) -> pd.DataFrame:
    """Convert one raw sheet to normalized long-form records."""

    cleaned = df.copy()
    cleaned.columns = [_normalize_column_name(col) for col in cleaned.columns]
    cleaned = cleaned.rename(columns={col: COLUMN_ALIASES.get(col, col) for col in cleaned.columns})
    cleaned = cleaned.dropna(how="all").drop_duplicates()

    if _looks_like_standard_metric_table(cleaned):
        return _standardize_metric_table(cleaned, source_label)
    return _convert_source_directory_table(cleaned, source_label)


def combine_and_clean(sheets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    frames = [clean_sheet(df, source_label=name) for name, df in sheets.items()]
    if not frames:
        return pd.DataFrame(columns=STANDARD_COLUMNS)
    combined = pd.concat(frames, ignore_index=True)
    combined = combined.drop_duplicates(subset=STANDARD_COLUMNS)
    return _ensure_schema(combined)


def _looks_like_standard_metric_table(df: pd.DataFrame) -> bool:
    required = {"metric_name", "metric_value"}
    return required.issubset(set(df.columns))


def _standardize_metric_table(df: pd.DataFrame, source_label: str) -> pd.DataFrame:
    output = df.copy()
    for col in STANDARD_COLUMNS:
        if col not in output.columns:
            output[col] = ""
    output["source_name"] = output["source_name"].replace("", pd.NA).fillna(source_label)
    output["source_type"] = output["source_type"].replace("", pd.NA).fillna("excel_metric_table")
    output["updated_date"] = output["updated_date"].replace("", pd.NA).fillna(today_iso())
    return _ensure_schema(output)


def _convert_source_directory_table(df: pd.DataFrame, source_label: str) -> pd.DataFrame:
    records = []
    for _, row in df.iterrows():
        countries = _split_multi_value(row.get("country", ""))
        platforms = _split_multi_value(row.get("platform", "")) or [""]
        metric_names = _split_multi_value(row.get("data_available", "")) or ["data_source"]
        countries = countries or [""]

        for country in countries:
            for platform in platforms:
                for metric_name in metric_names:
                    source_url = row.get("source_url", "") or row.get("search_url_example", "")
                    records.append(
                        {
                            "country": _clean_entity(country),
                            "industry": _clean_entity(row.get("industry", "")),
                            "product": _clean_entity(row.get("product", "")),
                            "platform": _clean_entity(platform),
                            "metric_name": _metric_slug(metric_name),
                            "metric_value": metric_name,
                            "metric_unit": "availability",
                            "source_name": _clean_entity(platform) or source_label,
                            "source_url": source_url if pd.notna(source_url) else "",
                            "source_type": "platform_data_source",
                            "updated_date": today_iso(),
                            "notes": _join_notes(
                                row.get("notes", ""),
                                row.get("suitable_for", ""),
                                row.get("ranking_url", ""),
                                row.get("search_url_example", ""),
                            ),
                        }
                    )
    return _ensure_schema(pd.DataFrame(records))


def _ensure_schema(df: pd.DataFrame) -> pd.DataFrame:
    for col in STANDARD_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    output = df[STANDARD_COLUMNS].copy()
    text_cols = [col for col in STANDARD_COLUMNS if col != "metric_value"]
    for col in text_cols:
        output[col] = output[col].fillna("").astype(str).map(lambda value: " ".join(value.split()))
    output["metric_value"] = output["metric_value"].fillna("")
    return output


def _normalize_column_name(value: object) -> str:
    name = str(value).strip().lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


def _split_multi_value(value: object) -> list[str]:
    if value is None or pd.isna(value):
        return []
    text = str(value)
    text = text.replace("；", ";").replace("|", ";")
    parts = re.split(r";|,", text)
    return [_clean_entity(part) for part in parts if _clean_entity(part) and _clean_entity(part).lower() != "more"]


def _clean_entity(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    text = " ".join(str(value).strip().split())
    if not text:
        return ""
    upper_map = {"us": "United States", "uk": "United Kingdom", "usa": "United States"}
    return upper_map.get(text.lower(), text.title() if text.isupper() else text)


def _metric_slug(value: object) -> str:
    text = str(value).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_") or "data_source"


def _join_notes(*values: Iterable[object]) -> str:
    parts = []
    for value in values:
        if value is not None and not pd.isna(value) and str(value).strip():
            parts.append(str(value).strip())
    return " | ".join(parts)

