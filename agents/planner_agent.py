"""Planner Agent: validates and normalizes a market-entry request."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MarketEntryTask:
    country: str
    industry: str
    product: str
    platform: str = ""
    objective: str = "Evaluate market entry opportunity"

    def to_dict(self) -> dict:
        return {
            "country": self.country,
            "industry": self.industry,
            "product": self.product,
            "platform": self.platform,
            "objective": self.objective,
        }


class PlannerAgent:
    """Turns raw user input into a structured task object."""

    REQUIRED_FIELDS = ("country", "industry", "product")

    def plan(self, country: str, industry: str, product: str, platform: str = "") -> dict:
        normalized = {
            "country": self._normalize(country),
            "industry": self._normalize(industry),
            "product": self._normalize(product),
            "platform": self._normalize(platform),
        }
        missing = [field for field in self.REQUIRED_FIELDS if not normalized[field]]
        if missing:
            raise ValueError(f"Missing required input: {', '.join(missing)}")
        return MarketEntryTask(**normalized).to_dict()

    @staticmethod
    def _normalize(value: str | None) -> str:
        if value is None:
            return ""
        cleaned = " ".join(str(value).strip().split())
        if cleaned.lower() in {"us", "usa", "united states of america"}:
            return "United States"
        if cleaned.lower() == "uk":
            return "United Kingdom"
        return cleaned.title() if cleaned.islower() or cleaned.isupper() else cleaned

