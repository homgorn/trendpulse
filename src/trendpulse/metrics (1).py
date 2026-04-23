from __future__ import annotations

import threading
from dataclasses import dataclass


@dataclass
class _MetricsState:
    requests_total: int = 0
    requests_success_total: int = 0
    requests_error_total: int = 0
    llm_latency_ms_sum: float = 0.0
    llm_latency_ms_count: int = 0


class MetricsRegistry:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._state = _MetricsState()

    def record_success(self, latency_ms: float) -> None:
        with self._lock:
            self._state.requests_total += 1
            self._state.requests_success_total += 1
            self._state.llm_latency_ms_sum += latency_ms
            self._state.llm_latency_ms_count += 1

    def record_error(self, latency_ms: float) -> None:
        with self._lock:
            self._state.requests_total += 1
            self._state.requests_error_total += 1
            self._state.llm_latency_ms_sum += latency_ms
            self._state.llm_latency_ms_count += 1

    def render_prometheus(self) -> str:
        with self._lock:
            s = self._state
            lines = [
                "# HELP trendpulse_requests_total Total generate requests",
                "# TYPE trendpulse_requests_total counter",
                f"trendpulse_requests_total {s.requests_total}",
                "# HELP trendpulse_requests_success_total Successful generate requests",
                "# TYPE trendpulse_requests_success_total counter",
                f"trendpulse_requests_success_total {s.requests_success_total}",
                "# HELP trendpulse_requests_error_total Failed generate requests",
                "# TYPE trendpulse_requests_error_total counter",
                f"trendpulse_requests_error_total {s.requests_error_total}",
                "# HELP trendpulse_llm_latency_ms_sum Sum of LLM request latency in milliseconds",
                "# TYPE trendpulse_llm_latency_ms_sum counter",
                f"trendpulse_llm_latency_ms_sum {s.llm_latency_ms_sum}",
                "# HELP trendpulse_llm_latency_ms_count Count of LLM latency observations",
                "# TYPE trendpulse_llm_latency_ms_count counter",
                f"trendpulse_llm_latency_ms_count {s.llm_latency_ms_count}",
            ]
            return "\n".join(lines) + "\n"


metrics = MetricsRegistry()
