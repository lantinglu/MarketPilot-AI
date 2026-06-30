from agents.planner_agent import PlannerAgent
from agents.retriever_agent import RetrieverAgent
from models.risk_model import RiskModel
from models.scoring_model import ScoringModel


def test_scoring_model_returns_weighted_score():
    task = PlannerAgent().plan("Japan", "Home & Kitchen", "Vacuum Flask")
    context = RetrieverAgent().retrieve(task)
    risk = RiskModel().assess(context)
    score = ScoringModel().score(context, risk)

    assert 0 <= score["total_score"] <= 100
    assert set(score["dimension_scores"].keys()) == set(ScoringModel.WEIGHTS.keys())

