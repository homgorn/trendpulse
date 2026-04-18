from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any


class LLMBackend(ABC):
    @abstractmethod
    async def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def stream_chat(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> AsyncIterator[str]:
        raise NotImplementedError

    @abstractmethod
    async def embed(
        self,
        texts: list[str],
        *,
        model: str | None = None,
    ) -> list[list[float]]:
        raise NotImplementedError
