from agents.planner_agent import PlannerAgent
from agents.retriever_agent import RetrieverAgent


def test_retriever_returns_context_for_sample_case():
    task = PlannerAgent().plan("Japan", "Home & Kitchen", "Vacuum Flask")
    context = RetrieverAgent().retrieve(task)

    assert context["metrics"]["population"] > 0
    assert context["metrics"]["average_price"] > 0
    assert "missing_fields" in context


def test_retriever_handles_unknown_input_gracefully():
    task = PlannerAgent().plan("Atlantis", "Unknown Category", "Mystery Product")
    context = RetrieverAgent().retrieve(task)

    assert isinstance(context["missing_fields"], list)
    assert context["metrics"]["population"] > 0


def test_planner_normalizes_country_aliases_and_codes():
    planner = PlannerAgent()

    assert planner.plan("USA", "Beauty", "Sunscreen")["country"] == "United States"
    assert planner.plan("United States of America", "Beauty", "Sunscreen")["country"] == "United States"
    assert planner.plan("DEU", "Consumer Electronics", "Wireless Earbuds")["country"] == "Germany"
    assert planner.plan("jp", "Home & Kitchen", "Vacuum Flask")["country"] == "Japan"
