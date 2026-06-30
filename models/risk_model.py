"""Market entry risk assessment model."""

from __future__ import annotations


class RiskModel:
    """Evaluates risk across saturation, pricing, regulatory, logistics, and cultural fit."""

    def assess(self, context: dict) -> dict:
        metrics = context["metrics"]
        risk_scores = {
            "Market saturation risk": self._clamp(metrics.get("competition_level", 6) * 12),
            "Pricing pressure risk": self._clamp(70 - metrics.get("average_price", 30) / 2 + metrics.get("competition_level", 6) * 5),
            "Regulatory risk": self._clamp(metrics.get("regulatory_complexity", 5) * 12),
            "Logistics risk": self._clamp(metrics.get("logistics_complexity", 4) * 12),
            "Cultural fit risk": self._clamp(100 - metrics.get("cultural_fit_score", 70)),
        }
        risk_score = round(sum(risk_scores.values()) / len(risk_scores), 1)
        return {
            "overall_risk": self._risk_level(risk_score),
            "risk_score": risk_score,
            "risk_factors": [
                f"{name}: {score:.1f}/100"
                for name, score in risk_scores.items()
                if score >= 50
            ]
            or ["No major risk factor above threshold."],
            "mitigation_suggestions": self._mitigations(risk_scores, context),
        }

    @staticmethod
    def _mitigations(risk_scores: dict, context: dict) -> list[str]:
        suggestions = []
        if risk_scores["Market saturation risk"] >= 50:
            suggestions.append("Differentiate through localized positioning, bundles, and early review generation.")
        if risk_scores["Pricing pressure risk"] >= 50:
            suggestions.append("Use a good-better-best price ladder and monitor competitor promotions weekly.")
        if risk_scores["Regulatory risk"] >= 50:
            suggestions.append("Validate labeling, import, safety, and certification requirements before inventory commitment.")
        if risk_scores["Logistics risk"] >= 50:
            suggestions.append("Start with conservative SKU depth and use local fulfillment or marketplace logistics.")
        if risk_scores["Cultural fit risk"] >= 50:
            suggestions.append("Localize messaging and product detail pages around the strongest consumer preference keywords.")
        if context.get("missing_fields"):
            suggestions.append("Replace fallback estimates with live marketplace and macro data before scaling.")
        return suggestions or ["Proceed with standard pilot controls and monthly risk review."]

    @staticmethod
    def _risk_level(score: float) -> str:
        if score >= 67:
            return "High"
        if score >= 40:
            return "Medium"
        return "Low"

    @staticmethod
    def _clamp(value: float, low: float = 0, high: float = 100) -> float:
        return max(low, min(high, float(value)))

