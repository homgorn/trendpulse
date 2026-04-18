from trendpulse.core.llm.routing import choose_route


def test_choose_route_reasoning_profile():
    decision = choose_route(task_type="reasoning")
    assert decision.profile == "reasoning"


def test_choose_route_low_cost_prefers_gemini():
    decision = choose_route(task_type="creative", budget_mode="low_cost")
    assert decision.provider == "gemini"
    assert decision.model == "gemini-2.0-flash"
