import time
from collections import defaultdict

from trendpulse.config import settings


class InMemoryRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.hits: dict[str, list[float]] = defaultdict(list)
        self._last_cleanup = time.time()
        self._cleanup_interval = 60.0

    def _maybe_cleanup(self) -> None:
        now = time.time()
        if now - self._last_cleanup > self._cleanup_interval:
            window_start = now - self.window_seconds
            dead_keys = [k for k, v in self.hits.items() if not any(t >= window_start for t in v)]
            for k in dead_keys:
                del self.hits[k]
            self._last_cleanup = now

    def is_allowed(self, key: str) -> tuple[bool, int]:
        self._maybe_cleanup()

        now = time.time()
        window_start = now - self.window_seconds

        self.hits[key] = [t for t in self.hits[key] if t >= window_start]

        if len(self.hits[key]) >= self.max_requests:
            oldest = min(self.hits[key])
            retry_after = int(self.window_seconds - (now - oldest)) + 1
            return False, retry_after

        self.hits[key].append(now)
        return True, self.max_requests - len(self.hits[key])


rate_limiter = InMemoryRateLimiter(
    max_requests=settings.rate_limit_requests,
    window_seconds=settings.rate_limit_window_seconds,
)
