"""Interpretable market entry scoring model."""

from __future__ import annotations


class ScoringModel:
    """Calculates a weighted 0-100 Market Entry Score."""

    WEIGHTS = {
        "Market Demand": 0.30,
        "Competition Intensity": 0.20,
        "Ecommerce Readiness": 0.20,
        "Pricing Potential": 0.15,
        "Risk Level": 0.15,
    }

    def score(self, context: dict, risk_result: dict | None = None) -> dict:
        metrics = context["metrics"]
        market_demand = self._clamp(
            metrics.get("industry_growth_rate", 0) * 5
            + metrics.get("review_volume", 0) / 1000
            + metrics.get("average_rating", 0) * 7
        )
        competition_intensity = self._clamp(100 - metrics.get("competition_level", 6) * 12)
        ecommerce_readiness = self._clamp(metrics.get("ecommerce_penetration", 0.55) * 100)
        pricing_potential = self._clamp(
            55
            + metrics.get("gdp_per_capita", 30000) / 2500
            + metrics.get("average_price", 30) / 2
            - metrics.get("competition_level", 6) * 8
        )
        risk_level = self._clamp(100 - risk_result["risk_score"]) if risk_result else 60

        dimension_scores = {
            "Market Demand": round(market_demand, 1),
            "Competition Intensity": round(competition_intensity, 1),
            "Ecommerce Readiness": round(ecommerce_readiness, 1),
            "Pricing Potential": round(pricing_potential, 1),
            "Risk Level": round(risk_level, 1),
        }
        total = sum(score * self.WEIGHTS[name] for name, score in dimension_scores.items())

        return {
            "total_score": round(total, 1),
            "dimension_scores": dimension_scores,
            "explanation": [
                "Market Demand blends category growth, review volume, and average rating.",
                "Competition Intensity is higher when the observed competition level is lower.",
                "Ecommerce Readiness reflects online commerce penetration for the target country.",
                "Pricing Potential considers GDP per capita, product price, and competitive pressure.",
                "Risk Level converts the risk model output into a positive score where lower risk is better.",
            ],
        }

    @staticmethod
    def _clamp(value: float, low: float = 0, high: float = 100) -> float:
        return max(low, min(high, float(value)))
