"""Retriever Agent: queries the standardized data layer and builds model context."""

from __future__ import annotations

from difflib import get_close_matches
from pathlib import Path
from typing import Any

import pandas as pd

from config import SAMPLE_DATASET_CSV, STANDARD_DATASET_CSV
from data_processing.build_dataset import build_dataset
from data_processing.data_schema import NUMERIC_METRICS, TEXT_METRICS


class RetrieverAgent:
    """Retrieves country, industry, product, platform, and source context."""

    def __init__(self, dataset_path: str | Path | None = None, auto_build: bool = True):
        self.dataset_path = Path(dataset_path or STANDARD_DATASET_CSV)
        if not self.dataset_path.exists() and auto_build:
            build_dataset()
        if not self.dataset_path.exists() and SAMPLE_DATASET_CSV.exists():
            self.dataset_path = SAMPLE_DATASET_CSV
        self.dataset = pd.read_csv(self.dataset_path)
        self.dataset["metric_name"] = self.dataset["metric_name"].fillna("").astype(str)

    def retrieve(self, task: dict) -> dict:
        matches = self._filter_records(task)
        fallback_records = self._fallback_records(task)
        combined = pd.concat([matches, fallback_records], ignore_index=True).drop_duplicates()

        metrics = self._extract_metrics(combined)
        missing_fields = self._missing_required_metrics(metrics)
        source_context = self._source_context(combined, task)

        return {
            "task": task,
            "metrics": metrics,
            "records": combined.to_dict(orient="records"),
            "source_context": source_context,
            "missing_fields": missing_fields,
            "data_quality": self._data_quality(matches, missing_fields),
        }

    def get_country_data(self, country: str) -> pd.DataFrame:
        return self._contains("country", country)

    def get_industry_data(self, industry: str) -> pd.DataFrame:
        return self._contains("industry", industry)

    def get_product_data(self, product: str) -> pd.DataFrame:
        return self._contains("product", product)

    def get_platform_data(self, platform: str) -> pd.DataFrame:
        return self._contains("platform", platform)

    def _filter_records(self, task: dict) -> pd.DataFrame:
        country = self._contains("country", task["country"])
        industry = self._contains("industry", task["industry"])
        product = self._contains("product", task["product"])

        mask = (
            self.dataset["country"].fillna("").str.lower().eq(task["country"].lower())
            & self.dataset["industry"].fillna("").str.lower().eq(task["industry"].lower())
            & self.dataset["product"].fillna("").str.lower().eq(task["product"].lower())
        )
        exact_combo = self.dataset[mask]
        frames = [exact_combo, country, industry, product]
        if task.get("platform"):
            frames.append(self.get_platform_data(task["platform"]))
        return pd.concat(frames, ignore_index=True).drop_duplicates()

    def _fallback_records(self, task: dict) -> pd.DataFrame:
        """Use nearest sample rows if exact metrics are not available."""

        sample = self.dataset[self.dataset["source_type"].fillna("") == "sample_estimate"]
        if sample.empty:
            return sample

        exact = sample[
            sample["country"].fillna("").str.lower().eq(task["country"].lower())
            & sample["industry"].fillna("").str.lower().eq(task["industry"].lower())
            & sample["product"].fillna("").str.lower().eq(task["product"].lower())
        ]
        if not exact.empty:
            return exact

        country_fallback = sample[sample["country"].fillna("").str.lower().eq(task["country"].lower())]
        if not country_fallback.empty:
            return country_fallback

        industry_fallback = sample[sample["industry"].fillna("").str.lower().eq(task["industry"].lower())]
        if not industry_fallback.empty:
            return industry_fallback

        return sample[sample["country"].fillna("").str.lower().eq("japan")]

    def _extract_metrics(self, records: pd.DataFrame) -> dict[str, Any]:
        metrics: dict[str, Any] = {}
        for metric in sorted(NUMERIC_METRICS | TEXT_METRICS):
            rows = records[records["metric_name"] == metric]
            if rows.empty:
                continue
            value = rows.iloc[0]["metric_value"]
            metrics[metric] = self._coerce_metric(metric, value)
        return metrics

    def _source_context(self, records: pd.DataFrame, task: dict) -> list[dict]:
        source_rows = records[records["source_type"].fillna("") == "platform_data_source"]
        if source_rows.empty:
            source_rows = self._contains("country", task["country"])
            source_rows = source_rows[source_rows["source_type"].fillna("") == "platform_data_source"]
        cols = ["country", "platform", "metric_name", "source_name", "source_url", "source_type", "notes"]
        return source_rows[cols].drop_duplicates().head(12).to_dict(orient="records")

    def _contains(self, column: str, value: str) -> pd.DataFrame:
        if not value:
            return self.dataset.iloc[0:0]
        series = self.dataset[column].fillna("").astype(str)
        direct = self.dataset[series.str.lower().str.contains(value.lower(), regex=False)]
        if not direct.empty:
            return direct

        choices = sorted(set(item for item in series.tolist() if item))
        close = get_close_matches(value, choices, n=1, cutoff=0.6)
        if close:
            return self.dataset[series == close[0]]
        return self.dataset.iloc[0:0]

    @staticmethod
    def _coerce_metric(metric: str, value: Any) -> Any:
        if metric not in NUMERIC_METRICS:
            return "" if pd.isna(value) else str(value)
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _missing_required_metrics(metrics: dict) -> list[str]:
        required = {
            "gdp_per_capita",
            "population",
            "ecommerce_penetration",
            "industry_growth_rate",
            "average_price",
            "average_rating",
            "review_volume",
            "competition_level",
            "regulatory_complexity",
            "logistics_complexity",
            "cultural_fit_score",
        }
        return sorted(metric for metric in required if metrics.get(metric) in {None, ""} or metric not in metrics)

    @staticmethod
    def _data_quality(matches: pd.DataFrame, missing_fields: list[str]) -> str:
        if missing_fields:
            return "partial_with_fallback"
        if matches.empty:
            return "fallback_only"
        if (matches["source_type"].fillna("") == "platform_data_source").any():
            return "excel_enriched"
        return "sample_complete"

