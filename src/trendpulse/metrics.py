from __future__ import annotations

import threading
from dataclasses import dataclass


@dataclass(slots=True)
class _ProviderMetrics:
    requests_total: int = 0
    requests_success_total: int = 0
    requests_error_total: int = 0
    requests_timeout_total: int = 0
    latency_ms_sum: float = 0.0
    latency_ms_count: int = 0
    tokens_total: int = 0
    estimated_cost_usd: float = 0.0


class MetricsRegistry:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._global_total = 0
        self._global_success = 0
        self._global_error = 0
        self._providers: dict[str, _ProviderMetrics] = {}

    def _get_provider(self, provider: str) -> _ProviderMetrics:
        if provider not in self._providers:
            self._providers[provider] = _ProviderMetrics()
        return self._providers[provider]

    def record_success(
        self,
        *,
        provider: str = "unknown",
        model: str = "unknown",
        latency_ms: float,
        tokens: int = 0,
        cost_usd: float = 0.0,
    ) -> None:
        with self._lock:
            self._global_total += 1
            self._global_success += 1
            p = self._get_provider(provider)
            p.requests_total += 1
            p.requests_success_total += 1
            p.latency_ms_sum += latency_ms
            p.latency_ms_count += 1
            p.tokens_total += tokens
            p.estimated_cost_usd += cost_usd

    def record_error(
        self,
        *,
        provider: str = "unknown",
        model: str = "unknown",
        latency_ms: float,
        error_type: str = "unknown",
    ) -> None:
        with self._lock:
            self._global_total += 1
            self._global_error += 1
            p = self._get_provider(provider)
            p.requests_total += 1
            p.requests_error_total += 1
            if error_type == "timeout":
                p.requests_timeout_total += 1
            p.latency_ms_sum += latency_ms
            p.latency_ms_count += 1

    def render_prometheus(self) -> str:
        with self._lock:
            lines: list[str] = []

            lines.append("# HELP trendpulse_requests_total Total generate requests")
            lines.append("# TYPE trendpulse_requests_total counter")
            lines.append(f"trendpulse_requests_total {self._global_total}")

            lines.append("# HELP trendpulse_requests_success_total Successful generate requests")
            lines.append("# TYPE trendpulse_requests_success_total counter")
            lines.append(f"trendpulse_requests_success_total {self._global_success}")

            lines.append("# HELP trendpulse_requests_error_total Failed generate requests")
            lines.append("# TYPE trendpulse_requests_error_total counter")
            lines.append(f"trendpulse_requests_error_total {self._global_error}")

            for provider, pm in self._providers.items():
                safe = provider.replace("-", "_").replace(".", "_")
                lines.append(f"# HELP trendpulse_provider_{safe}_requests_total Requests for {provider}")
                lines.append(f"# TYPE trendpulse_provider_{safe}_requests_total counter")
                lines.append(f"trendpulse_provider_{safe}_requests_total {pm.requests_total}")

                lines.append(f"# HELP trendpulse_provider_{safe}_latency_ms_sum Latency sum for {provider}")
                lines.append(f"# TYPE trendpulse_provider_{safe}_latency_ms_sum counter")
                lines.append(f"trendpulse_provider_{safe}_latency_ms_sum {pm.latency_ms_sum}")

                lines.append(f"# HELP trendpulse_provider_{safe}_latency_ms_count Latency count for {provider}")
                lines.append(f"# TYPE trendpulse_provider_{safe}_latency_ms_count counter")
                lines.append(f"trendpulse_provider_{safe}_latency_ms_count {pm.latency_ms_count}")

                if pm.tokens_total > 0:
                    lines.append(f"# HELP trendpulse_provider_{safe}_tokens_total Tokens used for {provider}")
                    lines.append(f"# TYPE trendpulse_provider_{safe}_tokens_total counter")
                    lines.append(f"trendpulse_provider_{safe}_tokens_total {pm.tokens_total}")

                if pm.estimated_cost_usd > 0:
                    lines.append(f"# HELP trendpulse_provider_{safe}_cost_usd_total Estimated cost for {provider}")
                    lines.append(f"# TYPE trendpulse_provider_{safe}_cost_usd_total counter")
                    lines.append(f"trendpulse_provider_{safe}_cost_usd_total {pm.estimated_cost_usd:.6f}")

            lines.append("# HELP trendpulse_llm_latency_ms_sum Sum of LLM request latency in milliseconds")
            lines.append("# TYPE trendpulse_llm_latency_ms_sum counter")
            total_sum = sum(pm.latency_ms_sum for pm in self._providers.values())
            lines.append(f"trendpulse_llm_latency_ms_sum {total_sum}")

            lines.append("# HELP trendpulse_llm_latency_ms_count Count of LLM latency observations")
            lines.append("# TYPE trendpulse_llm_latency_ms_count counter")
            total_count = sum(pm.latency_ms_count for pm in self._providers.values())
            lines.append(f"trendpulse_llm_latency_ms_count {total_count}")

            return "\n".join(lines) + "\n"

    def get_p50_latency(self) -> float:
        with self._lock:
            total_count = sum(pm.latency_ms_count for pm in self._providers.values())
            if total_count == 0:
                return 0.0
            total_sum = sum(pm.latency_ms_sum for pm in self._providers.values())
            return total_sum / total_count


metrics = MetricsRegistry()
