"""Command-line demo for Market Entry Agent."""

from __future__ import annotations

from config import OUTPUT_DIR
from agents.planner_agent import PlannerAgent
from agents.report_agent import ReportAgent
from agents.retriever_agent import RetrieverAgent
from models.demand_prediction_model import DemandPredictionModel
from models.risk_model import RiskModel
from models.scoring_model import ScoringModel


def run_market_entry_analysis(country: str, industry: str, product: str, platform: str = "") -> dict:
    planner = PlannerAgent()
    retriever = RetrieverAgent()
    risk_model = RiskModel()
    scoring_model = ScoringModel()
    demand_model = DemandPredictionModel()
    report_agent = ReportAgent()

    task = planner.plan(country=country, industry=industry, product=product, platform=platform)
    context = retriever.retrieve(task)
    risk_result = risk_model.assess(context)
    score_result = scoring_model.score(context, risk_result)
    demand_result = demand_model.predict(context)

    report_path = OUTPUT_DIR / "sample_report.md"
    report = report_agent.generate(
        context=context,
        score_result=score_result,
        demand_result=demand_result,
        risk_result=risk_result,
        output_path=report_path,
    )

    return {
        "task": task,
        "context": context,
        "score": score_result,
        "demand": demand_result,
        "risk": risk_result,
        "report": report,
        "report_path": report_path,
        "recommendation": _recommendation(score_result["total_score"], risk_result["overall_risk"]),
    }


def _recommendation(total_score: float, risk_level: str) -> str:
    if total_score >= 72 and risk_level != "High":
        return "Enter market with a focused pilot launch / 建议以聚焦型试点进入市场"
    if total_score >= 55:
        return "Enter cautiously after validation tests / 建议在完成验证测试后谨慎进入"
    return "Do not enter yet; improve positioning, pricing, or data confidence first / 暂不建议进入，先优化定位、价格或数据可信度"


if __name__ == "__main__":
    result = run_market_entry_analysis(
        country="Japan",
        industry="Home & Kitchen",
        product="Vacuum Flask",
    )

    print("Market Entry Agent")
    print("==================")
    print(f"Task: {result['task']}")
    print(f"Market Entry Score: {result['score']['total_score']}/100")
    print(f"Demand Level: {result['demand']['predicted_demand_level']}")
    print(f"Estimated Monthly Sales: {result['demand']['estimated_monthly_sales_range']}")
    print(f"Overall Risk: {result['risk']['overall_risk']} ({result['risk']['risk_score']}/100)")
    print(f"Recommendation: {result['recommendation']}")
    print(f"Data Quality: {result['context']['data_quality']}")
    print(f"Report generated: {result['report_path']}")
