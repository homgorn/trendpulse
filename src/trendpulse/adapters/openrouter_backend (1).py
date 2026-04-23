from typing import Any, AsyncIterator

import httpx

from trendpulse.core.llm.backends import LLMBackend
from trendpulse.errors import ProviderError, ProviderTimeoutError, ValidationError


class OpenRouterBackend(LLMBackend):
    def __init__(self, api_key: str, base_url: str = "https://openrouter.ai/api/v1"):
        if not api_key:
            raise ValidationError("OPENROUTER_API_KEY is required")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    async def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model or "openrouter/auto",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(url, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                return data["choices"][0]["message"]["content"]
        except httpx.TimeoutException as e:
            raise ProviderTimeoutError(f"OpenRouter timeout: {e}") from e
        except Exception as e:
            raise ProviderError(f"OpenRouter error: {e}") from e

    async def stream_chat(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> AsyncIterator[str]:
        text = await self.chat(
            messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        yield text

    async def embed(
        self,
        texts: list[str],
        *,
        model: str | None = None,
    ) -> list[list[float]]:
        # MVP-safe stub: deterministic pseudo-embedding for pipeline continuity.
        # Replace with provider embedding endpoint in next iteration.
        vectors: list[list[float]] = []
        for text in texts:
            seed = float(len(text) % 10) / 10.0
            vectors.append([seed, seed + 0.1, seed + 0.2, seed + 0.3])
        return vectors
