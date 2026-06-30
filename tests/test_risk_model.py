from agents.planner_agent import PlannerAgent
from agents.retriever_agent import RetrieverAgent
from models.risk_model import RiskModel


def test_risk_model_returns_expected_shape():
    task = PlannerAgent().plan("Germany", "Consumer Electronics", "Wireless Earbuds")
    context = RetrieverAgent().retrieve(task)
    risk = RiskModel().assess(context)

    assert risk["overall_risk"] in {"Low", "Medium", "High"}
    assert 0 <= risk["risk_score"] <= 100
    assert risk["risk_factors"]
    assert risk["mitigation_suggestions"]

