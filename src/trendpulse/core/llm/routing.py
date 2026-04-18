from dataclasses import dataclass


@dataclass(slots=True)
class RoutingDecision:
    provider: str
    model: str
    profile: str


def choose_route(
    *,
    task_type: str,
    budget_mode: str = "balanced",
    region: str = "global",
    default_provider: str = "openrouter",
    fallback_provider: str = "gemini",
    default_model: str = "openrouter/auto",
) -> RoutingDecision:
    profile = "balanced"

    if task_type in {"analysis", "reasoning"}:
        profile = "reasoning"
    elif task_type in {"ideation", "creative"}:
        profile = "creative"

    provider = default_provider
    model = default_model

    if budget_mode == "low_cost":
        provider = "gemini"
        model = "gemini-2.0-flash"

    if region.lower() in {"cn", "china"} and provider == fallback_provider:
        # Keep explicit for future region-aware policies
        provider = fallback_provider

    return RoutingDecision(provider=provider, model=model, profile=profile)
