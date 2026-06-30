"""Explainable demand prediction model for the MVP."""

from __future__ import annotations


class DemandPredictionModel:
    """Predicts demand using a transparent rules-based index."""

    def predict(self, context: dict) -> dict:
        metrics = context["metrics"]
        population_factor = min(metrics.get("population", 50_000_000) / 125_000_000, 2.0)
        wealth_factor = min(metrics.get("gdp_per_capita", 30000) / 45_000, 1.8)
        ecommerce_factor = metrics.get("ecommerce_penetration", 0.55) * 1.4
        growth_factor = metrics.get("industry_growth_rate", 5.0) / 10
        signal_factor = min(metrics.get("review_volume", 5000) / 12000, 1.6)
        rating_factor = metrics.get("average_rating", 4.0) / 5
        price_factor = max(0.45, 1.2 - metrics.get("average_price", 35) / 250)

        demand_index = (
            0.22 * population_factor
            + 0.15 * wealth_factor
            + 0.20 * ecommerce_factor
            + 0.16 * growth_factor
            + 0.15 * signal_factor
            + 0.07 * rating_factor
            + 0.05 * price_factor
        ) * 100

        monthly_midpoint = int(max(300, demand_index * 95))
        low = int(monthly_midpoint * 0.72)
        high = int(monthly_midpoint * 1.32)
        level = self._level(demand_index)

        return {
            "predicted_demand_level": level,
            "demand_index": round(demand_index, 1),
            "estimated_monthly_sales_range": f"{low:,} - {high:,} units",
            "explanation": (
                f"The demand index is {round(demand_index, 1)}/100 based on population, GDP per capita, "
                "ecommerce readiness, industry growth, review volume, rating, and price accessibility."
            ),
        }

    @staticmethod
    def _level(index: float) -> str:
        if index >= 75:
            return "High"
        if index >= 50:
            return "Medium"
        return "Low"

