"""Planner Agent: validates and normalizes a market-entry request."""

from __future__ import annotations

from dataclasses import dataclass

try:
    import pycountry
except ImportError:  # pragma: no cover - fallback keeps the MVP runnable without optional deps.
    pycountry = None


COUNTRY_ALIASES = {
    "america": "United States",
    "brasil": "Brazil",
    "britain": "United Kingdom",
    "ca": "Canada",
    "can": "Canada",
    "cn": "China",
    "chn": "China",
    "czech republic": "Czechia",
    "de": "Germany",
    "deu": "Germany",
    "england": "United Kingdom",
    "es": "Spain",
    "esp": "Spain",
    "fr": "France",
    "fra": "France",
    "gb": "United Kingdom",
    "gbr": "United Kingdom",
    "holland": "Netherlands",
    "hong kong": "Hong Kong",
    "in": "India",
    "ind": "India",
    "iran": "Iran, Islamic Republic of",
    "ivory coast": "Cote d'Ivoire",
    "jp": "Japan",
    "jpn": "Japan",
    "kr": "South Korea",
    "kor": "South Korea",
    "macau": "Macao",
    "mainland china": "China",
    "mx": "Mexico",
    "mex": "Mexico",
    "nl": "Netherlands",
    "nld": "Netherlands",
    "russia": "Russian Federation",
    "south korea": "South Korea",
    "taiwan": "Taiwan, Province of China",
    "tanzania": "Tanzania, United Republic of",
    "turkey": "Turkiye",
    "uae": "United Arab Emirates",
    "uk": "United Kingdom",
    "united states of america": "United States",
    "us": "United States",
    "usa": "United States",
    "viet nam": "Vietnam",
    "vietnam": "Vietnam",
}


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
            "country": self._normalize_country(country),
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
        return cleaned.title() if cleaned.islower() or cleaned.isupper() else cleaned

    @classmethod
    def _normalize_country(cls, value: str | None) -> str:
        cleaned = cls._normalize(value)
        if not cleaned:
            return ""

        alias = COUNTRY_ALIASES.get(cleaned.lower())
        if alias:
            return alias

        if pycountry is None:
            return cleaned

        country = pycountry.countries.get(alpha_2=cleaned.upper())
        if country:
            return country.name

        country = pycountry.countries.get(alpha_3=cleaned.upper())
        if country:
            return country.name

        try:
            return pycountry.countries.lookup(cleaned).name
        except LookupError:
            return cleaned
