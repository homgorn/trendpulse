import asyncio
from dataclasses import dataclass
from time import monotonic
from typing import Any

from trendpulse.adapters.gemini_backend import GeminiBackend
from trendpulse.adapters.openrouter_backend import OpenRouterBackend
from trendpulse.config import settings
from trendpulse.core.llm.routing import choose_route
from trendpulse.errors import ConfigurationError, ProviderError, ProviderTimeoutError
from trendpulse.logging_utils import get_logger


@dataclass(slots=True)
class LLMResult:
    text: str
    provider: str
    model: str
    profile: str


class LLMGateway:
    def __init__(self):
        self.backends: dict[str, Any] = {}
        self._provider_failures: dict[str, int] = {}
        self._circuit_open_until: dict[str, float] = {}

        if settings.openrouter_api_key:
            self.backends["openrouter"] = OpenRouterBackend(
                api_key=settings.openrouter_api_key,
                base_url=settings.openrouter_base_url,
            )
        if settings.gemini_api_key:
            self.backends["gemini"] = GeminiBackend(
                api_key=settings.gemini_api_key,
                base_url=settings.gemini_base_url,
            )

        if not self.backends:
            raise ConfigurationError("No LLM providers configured")

    async def chat(
        self,
        *,
        messages: list[dict[str, Any]],
        task_type: str = "analysis",
        budget_mode: str = "balanced",
        region: str = "global",
        trace_id: str | None = None,
    ) -> LLMResult:
        logger = get_logger("trendpulse.gateway", trace_id=trace_id)

        if not hasattr(self, "_provider_failures"):
            self._provider_failures = {}
        if not hasattr(self, "_circuit_open_until"):
            self._circuit_open_until = {}

        default_provider = getattr(settings, "default_provider", "openrouter")
        fallback_provider = getattr(settings, "fallback_provider", "gemini")
        default_model = getattr(settings, "default_model", "openrouter/auto")
        llm_max_retries = int(getattr(settings, "llm_max_retries", 1))
        llm_request_timeout_seconds = float(
            getattr(settings, "llm_request_timeout_seconds", 30.0)
        )
        llm_retry_backoff_seconds = float(
            getattr(settings, "llm_retry_backoff_seconds", 0.25)
        )
        llm_circuit_breaker_fail_threshold = int(
            getattr(settings, "llm_circuit_breaker_fail_threshold", 3)
        )
        llm_circuit_breaker_open_seconds = float(
            getattr(settings, "llm_circuit_breaker_open_seconds", 20.0)
        )

        decision = choose_route(
            task_type=task_type,
            budget_mode=budget_mode,
            region=region,
            default_provider=default_provider,
            fallback_provider=fallback_provider,
            default_model=default_model,
        )

        ordered = [decision.provider]
        if fallback_provider not in ordered:
            ordered.append(fallback_provider)
        for provider in self.backends.keys():
            if provider not in ordered:
                ordered.append(provider)

        last_error: Exception | None = None
        for provider in ordered:
            backend = self.backends.get(provider)
            if not backend:
                continue

            now = monotonic()
            open_until = self._circuit_open_until.get(provider, 0.0)
            if open_until > now:
                logger.warning(
                    f"Skipping provider={provider} circuit=open until={open_until:.3f}"
                )
                continue

            max_attempts = llm_max_retries + 1
            for attempt in range(1, max_attempts + 1):
                try:
                    logger.info(
                        f"Trying provider={provider} model={decision.model} attempt={attempt}/{max_attempts}"
                    )
                    text = await asyncio.wait_for(
                        backend.chat(messages, model=decision.model),
                        timeout=llm_request_timeout_seconds,
                    )
                    logger.info(f"Success provider={provider}")
                    self._provider_failures[provider] = 0
                    if provider in self._circuit_open_until:
                        self._circuit_open_until.pop(provider, None)

                    return LLMResult(
                        text=text,
                        provider=provider,
                        model=decision.model,
                        profile=decision.profile,
                    )
                except TimeoutError as e:
                    last_error = ProviderTimeoutError(
                        f"Provider timeout provider={provider} attempt={attempt}: {e}"
                    )
                except Exception as e:
                    last_error = e

                current_fails = self._provider_failures.get(provider, 0) + 1
                self._provider_failures[provider] = current_fails
                logger.warning(
                    f"Provider failed provider={provider} attempt={attempt}/{max_attempts} fails={current_fails} err={last_error}"
                )

                if current_fails >= llm_circuit_breaker_fail_threshold:
                    self._circuit_open_until[provider] = (
                        monotonic() + llm_circuit_breaker_open_seconds
                    )
                    logger.warning(
                        f"Circuit opened provider={provider} for={llm_circuit_breaker_open_seconds}s"
                    )
                    break

                if attempt < max_attempts:
                    await asyncio.sleep(llm_retry_backoff_seconds)

        raise ProviderError(f"All providers failed: {last_error}")
