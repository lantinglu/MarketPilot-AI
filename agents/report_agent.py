"""Report Agent: renders a client-ready bilingual market entry report."""

from __future__ import annotations

from pathlib import Path


class ReportAgent:
    """Generates a Chinese report followed by a full English report."""

    def generate(
        self,
        context: dict,
        score_result: dict,
        demand_result: dict,
        risk_result: dict,
        output_path: str | Path,
    ) -> str:
        report = "\n\n---\n\n".join(
            [
                self._render_chinese_report(context, score_result, demand_result, risk_result),
                self._render_english_report(context, score_result, demand_result, risk_result),
            ]
        )
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        return report

    def _render_chinese_report(
        self,
        context: dict,
        score_result: dict,
        demand_result: dict,
        risk_result: dict,
    ) -> str:
        task = context["task"]
        metrics = context["metrics"]
        recommendation = self._recommendation_cn(score_result["total_score"], risk_result["overall_risk"])

        return f"""# 市场进入分析报告

## 一、项目结论

本报告评估 **{task['product']}** 是否适合进入 **{task['country']}** 的 **{task['industry']}** 市场。基于当前数据，系统给出的市场进入评分为 **{score_result['total_score']}/100**，预测需求等级为 **{self._level_cn(demand_result['predicted_demand_level'])}**，综合风险等级为 **{self._level_cn(risk_result['overall_risk'])}**。

**最终建议：{recommendation}**

## 二、核心指标看板

| 指标 | 结果 |
| --- | ---: |
| 市场进入评分 | {score_result['total_score']}/100 |
| 需求指数 | {demand_result['demand_index']}/100 |
| 预计月销量 | {demand_result['estimated_monthly_sales_range']} |
| 综合风险分数 | {risk_result['risk_score']}/100 |
| 数据质量 | {self._data_quality_cn(context['data_quality'])} |

{self._benchmark_note_cn(context)}

## 三、目标市场概览

- 国家/地区：{task['country']}
- 人口规模：{self._fmt(metrics.get('population'), decimals=0)}
- 人均 GDP：${self._fmt(metrics.get('gdp_per_capita'), decimals=0)}
- 电商渗透率：{self._pct(metrics.get('ecommerce_penetration'))}
- 行业：{task['industry']}
- 行业增长率：{self._fmt(metrics.get('industry_growth_rate'))}%
- 关键趋势：{metrics.get('trend_keywords', '暂无数据')}

## 四、产品机会判断

- 产品：{task['product']}
- 平均价格：${self._fmt(metrics.get('average_price'))}
- 平均评分：{self._fmt(metrics.get('average_rating'))}/5
- 评论量：{self._fmt(metrics.get('review_volume'), decimals=0)}
- 消费者偏好关键词：{metrics.get('consumer_preference_keywords', '暂无数据')}

当前产品机会主要取决于三点：是否贴合本地消费者偏好，首发价格是否有竞争力，以及能否通过评论积累、达人验证和本地化商品页快速建立信任。若当前产品使用行业基准数据，则价格、评论量、竞争强度等指标代表该行业在目标市场的参考水平，而非该产品的实时平台数据。

## 五、竞争与平台环境

- 竞争强度：{self._fmt(metrics.get('competition_level'))}/10
- 主要平台：{metrics.get('main_platforms', self._platforms_from_sources(context))}
- 平台备注：{metrics.get('platform_notes', '建议结合平台数据源进一步验证类目动态。')}

可参考的数据来源：
{self._source_lines_cn(context['source_context'])}

## 六、需求预测

系统预测该产品需求等级为 **{self._level_cn(demand_result['predicted_demand_level'])}**，需求指数为 **{demand_result['demand_index']}/100**，预计月销量区间为 **{demand_result['estimated_monthly_sales_range']}**。

该预测综合考虑人口规模、人均 GDP、电商成熟度、行业增长、评论量、评分和价格可接受度。该结果适合作为早期市场判断，不应替代真实广告投放测试、关键词搜索量验证和平台竞品监控。

## 七、市场进入评分拆解

| 维度 | 得分 |
| --- | ---: |
{self._score_rows_cn(score_result['dimension_scores'])}

评分逻辑说明：
{self._bullet_lines(self._scoring_explanations_cn())}

## 八、风险评估

- 综合风险：**{self._level_cn(risk_result['overall_risk'])}**
- 风险分数：{risk_result['risk_score']}/100

主要风险：
{self._bullet_lines(self._risk_items_cn(risk_result['risk_factors']))}

缓解建议：
{self._bullet_lines(self._mitigations_cn(risk_result['mitigation_suggestions']))}

## 九、建议进入策略

- 推荐平台：{metrics.get('main_platforms', self._platforms_from_sources(context))}
- 定价建议：{self._pricing_suggestion_cn(metrics.get('average_price'))}
- 初期营销：建议先用平台搜索广告、评论积累、达人验证和本地化商品页文案做小规模验证。
- 目标消费者：{task['country']} 城市电商用户，关注 {task['industry']} 类目中可靠、好评、价格合理的产品。
- 决策建议：**{recommendation}**

## 十、数据质量说明

- 数据质量：{self._data_quality_cn(context['data_quality'])}
- 缺失字段：{', '.join(context['missing_fields']) if context['missing_fields'] else '无'}

本项目会保留 Excel 来源数据的元信息；只有在关键模型字段缺失时，才使用内置样例或行业基准估算数据作为兜底。正式用于客户决策前，建议补充实时平台数据、搜索趋势、竞品价格、广告点击成本和法规认证信息。
"""

    def _render_english_report(
        self,
        context: dict,
        score_result: dict,
        demand_result: dict,
        risk_result: dict,
    ) -> str:
        task = context["task"]
        metrics = context["metrics"]
        recommendation = self._recommendation_en(score_result["total_score"], risk_result["overall_risk"])

        return f"""# Market Entry Analysis Report

## 1. Executive Decision

This report evaluates whether **{task['product']}** should enter the **{task['industry']}** market in **{task['country']}**. Based on the current dataset, the Market Entry Score is **{score_result['total_score']}/100**, predicted demand is **{demand_result['predicted_demand_level']}**, and overall risk is **{risk_result['overall_risk']}**.

**Final recommendation: {recommendation}**

## 2. Executive Dashboard

| Metric | Result |
| --- | ---: |
| Market Entry Score | {score_result['total_score']}/100 |
| Demand Index | {demand_result['demand_index']}/100 |
| Estimated Monthly Sales | {demand_result['estimated_monthly_sales_range']} |
| Risk Score | {risk_result['risk_score']}/100 |
| Data Quality | {context['data_quality']} |

{self._benchmark_note_en(context)}

## 3. Target Market Overview

- Country: {task['country']}
- Population: {self._fmt(metrics.get('population'), decimals=0)}
- GDP per capita: ${self._fmt(metrics.get('gdp_per_capita'), decimals=0)}
- Ecommerce penetration: {self._pct(metrics.get('ecommerce_penetration'))}
- Industry: {task['industry']}
- Industry growth rate: {self._fmt(metrics.get('industry_growth_rate'))}%
- Key trend: {metrics.get('trend_keywords', 'Not available')}

## 4. Product Opportunity

- Product: {task['product']}
- Average price: ${self._fmt(metrics.get('average_price'))}
- Average rating: {self._fmt(metrics.get('average_rating'))}/5
- Review volume: {self._fmt(metrics.get('review_volume'), decimals=0)}
- Consumer preference keywords: {metrics.get('consumer_preference_keywords', 'Not available')}

The opportunity depends on matching local consumer preferences, setting a competitive launch price, and building early trust through reviews, creator validation, and localized product-page content. If the product uses industry benchmark data, price, review volume, and competition indicators represent the target industry's reference level rather than live product-level marketplace data.

## 5. Competitive And Platform Context

- Competition level: {self._fmt(metrics.get('competition_level'))}/10
- Main platforms: {metrics.get('main_platforms', self._platforms_from_sources(context))}
- Platform notes: {metrics.get('platform_notes', 'Use source context and marketplace checks to validate category-specific dynamics.')}

Relevant data sources:
{self._source_lines_en(context['source_context'])}

## 6. Demand Forecast

The predicted demand level is **{demand_result['predicted_demand_level']}**, with a demand index of **{demand_result['demand_index']}/100** and an estimated monthly sales range of **{demand_result['estimated_monthly_sales_range']}**.

The forecast combines population, GDP per capita, ecommerce readiness, industry growth, review volume, rating, and price accessibility. It should be treated as an early planning signal and validated with marketplace search volume, ad tests, and competitor monitoring.

## 7. Market Entry Score Breakdown

| Dimension | Score |
| --- | ---: |
{self._score_rows_en(score_result['dimension_scores'])}

Scoring rationale:
{self._bullet_lines(score_result['explanation'])}

## 8. Risk Assessment

- Overall risk: **{risk_result['overall_risk']}**
- Risk score: {risk_result['risk_score']}/100

Risk factors:
{self._bullet_lines(risk_result['risk_factors'])}

Mitigation suggestions:
{self._bullet_lines(risk_result['mitigation_suggestions'])}

## 9. Recommended Entry Strategy

- Recommended platforms: {metrics.get('main_platforms', self._platforms_from_sources(context))}
- Pricing suggestion: {self._pricing_suggestion_en(metrics.get('average_price'))}
- Initial marketing strategy: Launch with marketplace search ads, review generation, creator validation, and localized product-page copy.
- Target consumer profile: Urban ecommerce shoppers in {task['country']} looking for reliable products in the {task['industry']} category.
- Market entry decision: **{recommendation}**

## 10. Data Quality Note

- Data quality: {context['data_quality']}
- Missing fields: {', '.join(context['missing_fields']) if context['missing_fields'] else 'None'}

This project preserves source metadata from Excel-derived records and uses sample or industry benchmark estimates only when model-critical fields are unavailable. Before using the report for client decisions, add live marketplace data, search trends, competitor pricing, advertising costs, and regulatory requirements.
"""

    @staticmethod
    def _recommendation_cn(total_score: float, risk_level: str) -> str:
        if total_score >= 72 and risk_level != "High":
            return "建议以聚焦型试点进入市场"
        if total_score >= 55:
            return "建议在完成验证测试后谨慎进入"
        return "暂不建议进入，先优化定位、价格或数据可信度"

    @staticmethod
    def _recommendation_en(total_score: float, risk_level: str) -> str:
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
    def _level_cn(level: str) -> str:
        return {"High": "高", "Medium": "中", "Low": "低"}.get(level, level)

    @staticmethod
    def _data_quality_cn(value: str) -> str:
        labels = {
            "excel_enriched": "Excel 增强数据",
            "fallback_only": "仅使用兜底数据",
            "benchmark_estimate": "基准估算数据",
            "industry_benchmark": "行业基准估算数据",
            "partial_with_fallback": "部分字段使用兜底数据",
            "sample_complete": "完整样例数据",
        }
        return labels.get(value, value)

    @staticmethod
    def _benchmark_note_cn(context: dict) -> str:
        if context.get("data_quality") == "industry_benchmark":
            return "> 分析口径：当前产品暂无精确产品级指标，系统使用所选国家和行业的 benchmark 指标进行早期市场判断。"
        if context.get("data_quality") == "benchmark_estimate":
            return "> 分析口径：当前结果基于 benchmark 估算数据，适合用于 demo、初筛和方案比较。"
        return ""

    @staticmethod
    def _benchmark_note_en(context: dict) -> str:
        if context.get("data_quality") == "industry_benchmark":
            return "> Analysis basis: product-level metrics are not available, so the report uses benchmark metrics for the selected country and industry."
        if context.get("data_quality") == "benchmark_estimate":
            return "> Analysis basis: results are based on benchmark estimates and are suitable for demo, screening, and scenario comparison."
        return ""

    @staticmethod
    def _score_rows_en(scores: dict) -> str:
        return "\n".join(f"| {name} | {score} |" for name, score in scores.items())

    @staticmethod
    def _score_rows_cn(scores: dict) -> str:
        labels = {
            "Market Demand": "市场需求",
            "Competition Intensity": "竞争强度",
            "Ecommerce Readiness": "电商成熟度",
            "Pricing Potential": "定价潜力",
            "Risk Level": "风险水平",
        }
        return "\n".join(f"| {labels.get(name, name)} | {score} |" for name, score in scores.items())

    @staticmethod
    def _bullet_lines(items: list[str]) -> str:
        return "\n".join(f"- {item}" for item in items)

    @staticmethod
    def _platforms_from_sources(context: dict) -> str:
        platforms = sorted({row.get("platform", "") for row in context.get("source_context", []) if row.get("platform")})
        return ", ".join(platforms[:5]) if platforms else "待验证 / To be validated"

    @staticmethod
    def _source_lines_cn(source_context: list[dict]) -> str:
        if not source_context:
            return "- 暂无该市场的平台来源数据。"
        lines = []
        for source in source_context[:6]:
            label = source.get("source_name") or source.get("platform") or "Source"
            url = source.get("source_url") or "N/A"
            metric = source.get("metric_name") or "marketplace data"
            lines.append(f"- {label}: {metric} ({url})")
        return "\n".join(lines)

    @staticmethod
    def _source_lines_en(source_context: list[dict]) -> str:
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
    def _pricing_suggestion_cn(average_price) -> str:
        try:
            price = float(average_price)
            return f"建议首发价落在 ${price * 0.92:.2f} - ${price * 1.08:.2f} 附近，再测试组合装和启动优惠券。"
        except (TypeError, ValueError):
            return "建议用平台竞品价格设定首发价，并测试启动优惠券。"

    @staticmethod
    def _pricing_suggestion_en(average_price) -> str:
        try:
            price = float(average_price)
            return f"Start near ${price * 0.92:.2f} - ${price * 1.08:.2f}, then test bundles and launch coupons."
        except (TypeError, ValueError):
            return "Use platform benchmarks to set an entry price and test launch coupons."

    @staticmethod
    def _scoring_explanations_cn() -> list[str]:
        return [
            "市场需求综合类目增长、评论量和平均评分。",
            "竞争强度维度会在竞争水平较低时得到更高分。",
            "电商成熟度反映目标国家的线上消费渗透率。",
            "定价潜力综合人均 GDP、产品价格和竞争压力。",
            "风险水平会把风险模型结果转成正向分数，风险越低得分越高。",
        ]

    @staticmethod
    def _risk_items_cn(items: list[str]) -> list[str]:
        translations = {
            "Market saturation risk": "市场饱和风险",
            "Pricing pressure risk": "价格压力风险",
            "Regulatory risk": "法规风险",
            "Logistics risk": "物流风险",
            "Cultural fit risk": "文化匹配风险",
            "No major risk factor above threshold.": "暂无超过阈值的主要风险因素。",
        }
        translated = []
        for item in items:
            output = item
            for english, chinese in translations.items():
                output = output.replace(english, chinese)
            translated.append(output)
        return translated

    @staticmethod
    def _mitigations_cn(items: list[str]) -> list[str]:
        translations = {
            "Differentiate through localized positioning, bundles, and early review generation.": "通过本地化定位、组合装和早期评论积累形成差异化。",
            "Use a good-better-best price ladder and monitor competitor promotions weekly.": "使用基础款、进阶款、高端款价格梯度，并每周监控竞品促销。",
            "Validate labeling, import, safety, and certification requirements before inventory commitment.": "在备货前确认标签、进口、安全和认证要求。",
            "Start with conservative SKU depth and use local fulfillment or marketplace logistics.": "初期控制 SKU 深度，优先使用本地履约或平台物流。",
            "Localize messaging and product detail pages around the strongest consumer preference keywords.": "围绕最强消费者偏好关键词本地化营销信息和商品详情页。",
            "Replace fallback estimates with live marketplace and macro data before scaling.": "放量前用实时平台数据和宏观数据替换兜底估算。",
            "Proceed with standard pilot controls and monthly risk review.": "按标准试点机制推进，并进行月度风险复盘。",
        }
        return [translations.get(item, item) for item in items]
