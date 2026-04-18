from collections.abc import AsyncIterator
from typing import Any

import httpx

from trendpulse.core.llm.backends import LLMBackend
from trendpulse.errors import ProviderError, ProviderTimeoutError, ValidationError


class GeminiBackend(LLMBackend):
    def __init__(self, api_key: str, base_url: str = "https://generativelanguage.googleapis.com"):
        if not api_key:
            raise ValidationError("GEMINI_API_KEY is required")
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
        model_name = model or "gemini-2.0-flash"
        url = f"{self.base_url}/v1beta/models/{model_name}:generateContent?key={self.api_key}"

        contents = []
        for msg in messages:
            role = msg.get("role", "user")
            if role == "system":
                role = "model"
            content = str(msg.get("content", ""))
            contents.append({"role": role, "parts": [{"text": content}]})

        payload = {
            "contents": contents,
            "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens},
        }
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(url, json=payload)
                resp.raise_for_status()
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except httpx.TimeoutException as e:
            raise ProviderTimeoutError(f"Gemini timeout: {e}") from e
        except Exception as e:
            raise ProviderError(f"Gemini error: {e}") from e

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
        raise NotImplementedError("Gemini embedding not implemented - use OpenRouter or external service")
