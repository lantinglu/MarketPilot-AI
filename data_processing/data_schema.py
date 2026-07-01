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

    market_specs = _benchmark_market_specs() + [
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
        spec_source = spec.get("source", source)
        base = {
            "country": spec["country"],
            "industry": spec["industry"],
            "product": spec["product"],
            "platform": spec["platform"],
            **spec_source,
        }
        for metric_name, metric_value in spec.items():
            if metric_name in {"country", "industry", "product", "platform", "source"}:
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


def _benchmark_market_specs() -> list[dict]:
    """Estimated benchmark scenarios for a richer portfolio demo.

    These records are intentionally marked as benchmark estimates. They are
    suitable for product-demo scenario comparisons, not as live market data.
    """

    source = {
        "source_name": "Cross-border Benchmark Dataset",
        "source_url": "local://data/sample/sample_market_entry_dataset.csv",
        "source_type": "benchmark_estimate",
        "updated_date": today_iso(),
    }
    country_profiles = {
        "United States": {
            "gdp_per_capita": 76000,
            "population": 335000000,
            "ecommerce_penetration": 0.82,
            "regulatory_complexity": 4.2,
            "logistics_complexity": 3.5,
            "cultural_fit_score": 78,
            "platforms": "Amazon, Walmart Marketplace, Target",
            "platform": "Amazon",
            "platform_notes": "Large market with high ad competition and strong review dependence.",
        },
        "Hong Kong": {
            "gdp_per_capita": 50000,
            "population": 7500000,
            "ecommerce_penetration": 0.78,
            "regulatory_complexity": 3.2,
            "logistics_complexity": 2.2,
            "cultural_fit_score": 86,
            "platforms": "HKTVmall, Amazon Global, Zalora",
            "platform": "HKTVmall",
            "platform_notes": "Compact high-income market with fast fulfillment expectations.",
        },
        "Japan": {
            "gdp_per_capita": 34000,
            "population": 123000000,
            "ecommerce_penetration": 0.74,
            "regulatory_complexity": 5.0,
            "logistics_complexity": 3.0,
            "cultural_fit_score": 82,
            "platforms": "Amazon Japan, Rakuten, Yahoo Shopping",
            "platform": "Amazon Japan",
            "platform_notes": "Quality, packaging, reviews, and seasonal promotion calendars matter.",
        },
        "South Korea": {
            "gdp_per_capita": 33000,
            "population": 52000000,
            "ecommerce_penetration": 0.88,
            "regulatory_complexity": 5.0,
            "logistics_complexity": 2.8,
            "cultural_fit_score": 80,
            "platforms": "Coupang, Naver Shopping, Gmarket",
            "platform": "Coupang",
            "platform_notes": "Fast delivery, localized content, and influencer validation are important.",
        },
        "Vietnam": {
            "gdp_per_capita": 4300,
            "population": 100000000,
            "ecommerce_penetration": 0.58,
            "regulatory_complexity": 5.8,
            "logistics_complexity": 5.2,
            "cultural_fit_score": 72,
            "platforms": "Shopee Vietnam, Lazada Vietnam, TikTok Shop",
            "platform": "Shopee Vietnam",
            "platform_notes": "Price sensitivity is high; social commerce and promotions drive demand.",
        },
        "Germany": {
            "gdp_per_capita": 52000,
            "population": 84000000,
            "ecommerce_penetration": 0.79,
            "regulatory_complexity": 5.8,
            "logistics_complexity": 3.2,
            "cultural_fit_score": 74,
            "platforms": "Amazon Germany, Otto, MediaMarkt",
            "platform": "Amazon Germany",
            "platform_notes": "Compliance, warranty messaging, and delivery reliability matter.",
        },
        "Netherlands": {
            "gdp_per_capita": 61000,
            "population": 18000000,
            "ecommerce_penetration": 0.84,
            "regulatory_complexity": 5.2,
            "logistics_complexity": 2.6,
            "cultural_fit_score": 77,
            "platforms": "Bol.com, Amazon Netherlands, Coolblue",
            "platform": "Bol.com",
            "platform_notes": "High ecommerce maturity and strong logistics infrastructure.",
        },
        "Malaysia": {
            "gdp_per_capita": 12000,
            "population": 34000000,
            "ecommerce_penetration": 0.68,
            "regulatory_complexity": 4.8,
            "logistics_complexity": 4.2,
            "cultural_fit_score": 76,
            "platforms": "Shopee Malaysia, Lazada Malaysia, TikTok Shop",
            "platform": "Shopee Malaysia",
            "platform_notes": "Marketplace promotions, halal awareness, and mobile shopping are important.",
        },
    }
    product_profiles = {
        "Beauty": {
            "product": "Sunscreen",
            "industry_growth_rate": 8.2,
            "average_price": 18,
            "average_rating": 4.3,
            "review_volume": 13500,
            "competition_level": 7.2,
            "trend_keywords": "sun care, clean beauty, sensitive skin, daily SPF",
            "consumer_preference_keywords": "lightweight texture, SPF50, no white cast, sensitive skin",
        },
        "Home & Kitchen": {
            "product": "Vacuum Flask",
            "industry_growth_rate": 6.1,
            "average_price": 28,
            "average_rating": 4.5,
            "review_volume": 8200,
            "competition_level": 6.4,
            "trend_keywords": "portable hydration, thermal insulation, sustainable materials",
            "consumer_preference_keywords": "leak-proof, heat retention, compact, minimalist design",
        },
        "Consumer Electronics": {
            "product": "Wireless Earbuds",
            "industry_growth_rate": 5.6,
            "average_price": 55,
            "average_rating": 4.2,
            "review_volume": 24500,
            "competition_level": 8.2,
            "trend_keywords": "wireless audio, mobile accessories, noise cancelling",
            "consumer_preference_keywords": "battery life, compact case, stable bluetooth, warranty",
        },
        "Pet Supplies": {
            "product": "Pet Grooming Brush",
            "industry_growth_rate": 7.4,
            "average_price": 16,
            "average_rating": 4.4,
            "review_volume": 6800,
            "competition_level": 5.8,
            "trend_keywords": "pet humanization, home grooming, shedding control",
            "consumer_preference_keywords": "safe bristles, easy cleaning, ergonomic grip, fur removal",
        },
        "Sports & Outdoors": {
            "product": "Resistance Bands",
            "industry_growth_rate": 6.9,
            "average_price": 22,
            "average_rating": 4.3,
            "review_volume": 9200,
            "competition_level": 6.9,
            "trend_keywords": "home fitness, portable workout, rehabilitation training",
            "consumer_preference_keywords": "durable latex, multiple resistance levels, travel pouch, workout guide",
        },
    }

    country_adjustments = {
        "United States": {"growth": 1.05, "reviews": 1.35, "competition": 1.10, "price": 1.10},
        "Hong Kong": {"growth": 0.95, "reviews": 0.70, "competition": 0.95, "price": 1.18},
        "Japan": {"growth": 0.98, "reviews": 0.90, "competition": 1.00, "price": 1.08},
        "South Korea": {"growth": 1.08, "reviews": 1.05, "competition": 1.08, "price": 1.02},
        "Vietnam": {"growth": 1.25, "reviews": 0.62, "competition": 0.86, "price": 0.72},
        "Germany": {"growth": 0.90, "reviews": 0.95, "competition": 1.06, "price": 1.12},
        "Netherlands": {"growth": 0.92, "reviews": 0.80, "competition": 0.98, "price": 1.15},
        "Malaysia": {"growth": 1.18, "reviews": 0.72, "competition": 0.92, "price": 0.82},
    }

    specs = []
    for country, country_profile in country_profiles.items():
        adjustments = country_adjustments[country]
        for industry, product_profile in product_profiles.items():
            specs.append(
                {
                    "country": country,
                    "industry": industry,
                    "product": product_profile["product"],
                    "platform": country_profile["platform"],
                    "gdp_per_capita": country_profile["gdp_per_capita"],
                    "population": country_profile["population"],
                    "ecommerce_penetration": country_profile["ecommerce_penetration"],
                    "regulatory_complexity": country_profile["regulatory_complexity"],
                    "logistics_complexity": country_profile["logistics_complexity"],
                    "industry_growth_rate": round(product_profile["industry_growth_rate"] * adjustments["growth"], 1),
                    "average_price": round(product_profile["average_price"] * adjustments["price"], 1),
                    "average_rating": product_profile["average_rating"],
                    "review_volume": int(product_profile["review_volume"] * adjustments["reviews"]),
                    "competition_level": round(min(9.5, product_profile["competition_level"] * adjustments["competition"]), 1),
                    "cultural_fit_score": country_profile["cultural_fit_score"],
                    "trend_keywords": product_profile["trend_keywords"],
                    "consumer_preference_keywords": product_profile["consumer_preference_keywords"],
                    "main_platforms": country_profile["platforms"],
                    "platform_notes": country_profile["platform_notes"],
                    "source": source,
                }
            )
    return specs


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
