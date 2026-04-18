# LLM Backend Interface v1

## Цель

Определить provider-agnostic контракт для LLM-слоя TrendPulse.

## Python Interface (reference)

```python
from abc import ABC, abstractmethod
from typing import AsyncIterator, List, Dict, Any

class LLMBackend(ABC):
    @abstractmethod
    async def chat(
        self,
        messages: List[Dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str: ...

    @abstractmethod
    async def stream_chat(
        self,
        messages: List[Dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> AsyncIterator[str]: ...

    @abstractmethod
    async def embed(
        self,
        texts: List[str],
        *,
        model: str | None = None,
    ) -> List[List[float]]: ...
```

## Behavioral Contract

1. Backend не должен “протекать” provider-specific типами наружу.
2. Ошибки маппятся в унифицированные доменные исключения.
3. Для `chat` обязателен deterministic режим при `temperature=0`.
4. Для `stream_chat` обязателен graceful завершение стрима при сетевых сбоях с понятной ошибкой.
5. Для `embed` размерность вектора документируется в metadata ответа/логе.

## Required Metadata (per request)

- provider_name
- model_name
- request_id / trace_id
- latency_ms
- token_usage (if available)
- estimated_cost (if available)

## Test Contract (minimum)

1. Chat happy-path.
2. Chat provider-timeout path.
3. Stream partial chunks + completion.
4. Embed single/batch inputs.
5. Empty/invalid input validation.
