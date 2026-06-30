"""Report Agent: renders a Markdown market entry report."""

from __future__ import annotations

from pathlib import Path


class ReportAgent:
    """Generates a professional Markdown report from model outputs."""

    def generate(
        self,
        context: dict,
        score_result: dict,
        demand_result: dict,
        risk_result: dict,
        output_path: str | Path,
    ) -> str:
        task = context["task"]
        metrics = context["metrics"]
        recommendation = self._recommendation(score_result["total_score"], risk_result["overall_risk"])

        report = f"""# Market Entry Report

## 1. Executive Summary

This report evaluates whether **{task['product']}** should enter the **{task['industry']}** market in **{task['country']}**. The Market Entry Score is **{score_result['total_score']}/100**, predicted demand is **{demand_result['predicted_demand_level']}**, and overall risk is **{risk_result['overall_risk']}**.

Final recommendation: **{recommendation}**

## 2. Market Overview

- Country: {task['country']}
- Population: {self._fmt(metrics.get('population'), decimals=0)}
- GDP per capita: ${self._fmt(metrics.get('gdp_per_capita'), decimals=0)}
- Ecommerce penetration: {self._pct(metrics.get('ecommerce_penetration'))}
- Industry: {task['industry']}
- Industry growth rate: {self._fmt(metrics.get('industry_growth_rate'))}%
- Key industry trend: {metrics.get('trend_keywords', 'Not available')}

## 3. Product Opportunity

- Product: {task['product']}
- Average price: ${self._fmt(metrics.get('average_price'))}
- Average rating: {self._fmt(metrics.get('average_rating'))}/5
- Review volume: {self._fmt(metrics.get('review_volume'), decimals=0)}
- Consumer preference keywords: {metrics.get('consumer_preference_keywords', 'Not available')}

The product opportunity depends on matching local consumer preferences, pricing at a competitive entry point, and building trust signals quickly through reviews and platform-native content.

## 4. Competition Analysis

- Competition level: {self._fmt(metrics.get('competition_level'))}/10
- Main platforms: {metrics.get('main_platforms', self._platforms_from_sources(context))}
- Platform notes: {metrics.get('platform_notes', 'Use source context and marketplace checks to validate category-specific dynamics.')}

Relevant data sources:
{self._source_lines(context['source_context'])}

## 5. Demand Prediction

- Predicted demand level: **{demand_result['predicted_demand_level']}**
- Demand index: {demand_result['demand_index']}/100
- Estimated monthly sales range: **{demand_result['estimated_monthly_sales_range']}**

{demand_result['explanation']}

## 6. Market Entry Score

- Total score: **{score_result['total_score']}/100**

| Dimension | Score |
| --- | ---: |
{self._score_rows(score_result['dimension_scores'])}

Scoring explanation:
{self._bullet_lines(score_result['explanation'])}

## 7. Risk Assessment

- Overall risk: **{risk_result['overall_risk']}**
- Risk score: {risk_result['risk_score']}/100

Risk factors:
{self._bullet_lines(risk_result['risk_factors'])}

Mitigation suggestions:
{self._bullet_lines(risk_result['mitigation_suggestions'])}

## 8. Recommended Entry Strategy

- Recommended platforms: {metrics.get('main_platforms', self._platforms_from_sources(context))}
- Pricing suggestion: {self._pricing_suggestion(metrics.get('average_price'))}
- Initial marketing strategy: Launch with marketplace search ads, review generation, creator validation, and localized product-page copy around {metrics.get('consumer_preference_keywords', 'local consumer needs')}.
- Target consumer profile: Urban ecommerce shoppers in {task['country']} looking for reliable products in the {task['industry']} category.
- Market entry decision: **{recommendation}**

## Data Quality Note

- Data quality: **{context['data_quality']}**
- Missing fields: {', '.join(context['missing_fields']) if context['missing_fields'] else 'None'}

This project preserves source metadata from Excel-derived records and uses sample fallback estimates only when model-critical fields are unavailable.
"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        return report

    @staticmethod
    def _recommendation(total_score: float, risk_level: str) -> str:
        if total_score >= 72 and risk_level != "High":
            return "Enter market with a focused pilot launch"
        if total_score >= 55:
            return "Enter cautiously after validation tests"
        return "Do not enter yet; improve positioning, pricing, or data confidence first"

    @staticmethod
    def _fmt(value, decimals: int = 1) -> str:
        if value is None or value == "":
            return "N/A"
        try:
            number = float(value)
            if decimals == 0:
                return f"{number:,.0f}"
            return f"{number:,.{decimals}f}".rstrip("0").rstrip(".")
        except (TypeError, ValueError):
            return str(value)

    @staticmethod
    def _pct(value) -> str:
        try:
            return f"{float(value):.0%}"
        except (TypeError, ValueError):
            return "N/A"

    @staticmethod
    def _score_rows(scores: dict) -> str:
        return "\n".join(f"| {name} | {score} |" for name, score in scores.items())

    @staticmethod
    def _bullet_lines(items: list[str]) -> str:
        return "\n".join(f"- {item}" for item in items)

    @staticmethod
    def _source_lines(source_context: list[dict]) -> str:
        if not source_context:
            return "- No platform source rows available for this market."
        lines = []
        for source in source_context[:6]:
            label = source.get("source_name") or source.get("platform") or "Source"
            url = source.get("source_url") or "N/A"
            metric = source.get("metric_name") or "marketplace data"
            lines.append(f"- {label}: {metric} ({url})")
        return "\n".join(lines)

    @staticmethod
    def _platforms_from_sources(context: dict) -> str:
        platforms = sorted({row.get("platform", "") for row in context.get("source_context", []) if row.get("platform")})
        return ", ".join(platforms[:5]) if platforms else "To be validated"

    @staticmethod
    def _pricing_suggestion(average_price) -> str:
        try:
            price = float(average_price)
            return f"Start near ${price * 0.92:.2f} - ${price * 1.08:.2f}, then test bundles and launch coupons."
        except (TypeError, ValueError):
            return "Use platform benchmarks to set an entry price and test launch coupons."

