"""Canonical schema and sample records for the market entry data layer."""

from __future__ import annotations

from datetime import date


STANDARD_COLUMNS = [
    "country",
    "industry",
    "product",
    "platform",
    "metric_name",
    "metric_value",
    "metric_unit",
    "source_name",
    "source_url",
    "source_type",
    "updated_date",
    "notes",
]

NUMERIC_METRICS = {
    "gdp_per_capita",
    "population",
    "ecommerce_penetration",
    "regulatory_complexity",
    "logistics_complexity",
    "industry_growth_rate",
    "average_price",
    "average_rating",
    "review_volume",
    "competition_level",
    "cultural_fit_score",
}

TEXT_METRICS = {
    "trend_keywords",
    "consumer_preference_keywords",
    "main_platforms",
    "platform_notes",
    "data_available",
    "suitable_for",
    "search_url_example",
    "ranking_url",
}


def today_iso() -> str:
    return date.today().isoformat()


def sample_records() -> list[dict]:
    """Fallback records that make the repo runnable without private data."""

    updated = today_iso()
    source = {
        "source_name": "MVP Sample Dataset",
        "source_url": "local://data/sample/sample_market_entry_dataset.csv",
        "source_type": "sample_estimate",
        "updated_date": updated,
    }

    market_specs = [
        {
            "country": "Japan",
            "industry": "Home & Kitchen",
            "product": "Vacuum Flask",
            "platform": "Amazon Japan",
            "gdp_per_capita": 34000,
            "population": 123000000,
            "ecommerce_penetration": 0.74,
            "regulatory_complexity": 5.0,
            "logistics_complexity": 3.0,
            "industry_growth_rate": 6.8,
            "average_price": 28,
            "average_rating": 4.5,
            "review_volume": 8200,
            "competition_level": 6.2,
            "cultural_fit_score": 82,
            "trend_keywords": "compact living, premium utility, sustainable materials",
            "consumer_preference_keywords": "compact, leak-proof, heat retention, minimalist design",
            "main_platforms": "Amazon Japan, Rakuten, Yahoo Shopping",
            "platform_notes": "Marketplace reviews and seasonal promotion calendars matter.",
        },
        {
            "country": "United States",
            "industry": "Beauty",
            "product": "Sunscreen",
            "platform": "Amazon",
            "gdp_per_capita": 76000,
            "population": 335000000,
            "ecommerce_penetration": 0.82,
            "regulatory_complexity": 4.0,
            "logistics_complexity": 3.5,
            "industry_growth_rate": 8.5,
            "average_price": 18,
            "average_rating": 4.3,
            "review_volume": 14500,
            "competition_level": 7.0,
            "cultural_fit_score": 78,
            "trend_keywords": "sun care, clean beauty, dermocosmetics",
            "consumer_preference_keywords": "lightweight texture, SPF50, sensitive skin, no white cast",
            "main_platforms": "Amazon, Walmart Marketplace, Target",
            "platform_notes": "Search ranking, ratings, ingredient claims, and seasonal demand are critical.",
        },
        {
            "country": "Germany",
            "industry": "Consumer Electronics",
            "product": "Wireless Earbuds",
            "platform": "Amazon Germany",
            "gdp_per_capita": 52000,
            "population": 84000000,
            "ecommerce_penetration": 0.79,
            "regulatory_complexity": 5.5,
            "logistics_complexity": 3.0,
            "industry_growth_rate": 5.4,
            "average_price": 55,
            "average_rating": 4.2,
            "review_volume": 26000,
            "competition_level": 8.3,
            "cultural_fit_score": 74,
            "trend_keywords": "wireless audio, mobile accessories, smart devices",
            "consumer_preference_keywords": "noise cancelling, battery life, compact case, warranty",
            "main_platforms": "Amazon Germany, Otto, MediaMarkt",
            "platform_notes": "Compliance, warranty messaging, and delivery reliability matter.",
        },
    ]

    records = []
    for spec in market_specs:
        base = {
            "country": spec["country"],
            "industry": spec["industry"],
            "product": spec["product"],
            "platform": spec["platform"],
            **source,
        }
        for metric_name, metric_value in spec.items():
            if metric_name in {"country", "industry", "product", "platform"}:
                continue
            records.append(
                {
                    **base,
                    "metric_name": metric_name,
                    "metric_value": metric_value,
                    "metric_unit": _unit_for(metric_name),
                    "notes": "Sample fallback metric for standalone demo runs.",
                }
            )
    return records


def _unit_for(metric_name: str) -> str:
    if metric_name in {"ecommerce_penetration"}:
        return "ratio"
    if metric_name in {"industry_growth_rate"}:
        return "percent"
    if metric_name in {"average_price", "gdp_per_capita"}:
        return "usd"
    if metric_name in {"population", "review_volume"}:
        return "count"
    if metric_name in {"average_rating"}:
        return "rating_1_to_5"
    if metric_name in {"competition_level", "regulatory_complexity", "logistics_complexity"}:
        return "score_1_to_10"
    if metric_name in {"cultural_fit_score"}:
        return "score_0_to_100"
    return "text"

