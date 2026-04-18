import asyncio

import pytest

from trendpulse.core.llm.gateway import LLMGateway
from trendpulse.errors import ProviderError


class _FakeBackendOk:
    async def chat(self, messages, model=None, temperature=0.7, max_tokens=2048):
        return '{"idea":"x","audience":"y","monetization":"z","risks":[],"sources":[]}'


class _FakeBackendFail:
    async def chat(self, messages, model=None, temperature=0.7, max_tokens=2048):
        raise RuntimeError("boom")


class _FakeBackendTimeout:
    async def chat(self, messages, model=None, temperature=0.7, max_tokens=2048):
        raise TimeoutError("timeout")


class _FlakyBackend:
    def __init__(self):
        self.calls = 0

    async def chat(self, messages, model=None, temperature=0.7, max_tokens=2048):
        self.calls += 1
        if self.calls == 1:
            raise RuntimeError("first fail")
        return '{"idea":"x","audience":"y","monetization":"z","risks":[],"sources":[]}'


@pytest.mark.asyncio
async def test_gateway_fallback_success():
    gw = object.__new__(LLMGateway)
    gw.backends = {"openrouter": _FakeBackendFail(), "gemini": _FakeBackendOk()}

    from trendpulse.core.llm import gateway as gw_mod

    old_settings = gw_mod.settings

    class _S:
        default_provider = "openrouter"
        fallback_provider = "gemini"
        default_model = "openrouter/auto"
        llm_max_retries = 0
        llm_request_timeout_seconds = 1.0
        llm_retry_backoff_seconds = 0.0
        llm_circuit_breaker_fail_threshold = 3
        llm_circuit_breaker_open_seconds = 10.0

    gw_mod.settings = _S()

    try:
        result = await gw.chat(messages=[{"role": "user", "content": "hi"}])
        assert result.provider == "gemini"
    finally:
        gw_mod.settings = old_settings


@pytest.mark.asyncio
async def test_gateway_all_fail():
    gw = object.__new__(LLMGateway)
    gw.backends = {"openrouter": _FakeBackendFail(), "gemini": _FakeBackendFail()}

    from trendpulse.core.llm import gateway as gw_mod

    old_settings = gw_mod.settings

    class _S:
        default_provider = "openrouter"
        fallback_provider = "gemini"
        default_model = "openrouter/auto"
        llm_max_retries = 0
        llm_request_timeout_seconds = 1.0
        llm_retry_backoff_seconds = 0.0
        llm_circuit_breaker_fail_threshold = 3
        llm_circuit_breaker_open_seconds = 10.0

    gw_mod.settings = _S()

    try:
        with pytest.raises(ProviderError):
            await gw.chat(messages=[{"role": "user", "content": "hi"}])
    finally:
        gw_mod.settings = old_settings


@pytest.mark.asyncio
async def test_gateway_retry_then_success():
    gw = object.__new__(LLMGateway)
    flaky = _FlakyBackend()
    gw.backends = {"openrouter": flaky}

    from trendpulse.core.llm import gateway as gw_mod

    old_settings = gw_mod.settings

    class _S:
        default_provider = "openrouter"
        fallback_provider = "gemini"
        default_model = "openrouter/auto"
        llm_max_retries = 1
        llm_request_timeout_seconds = 1.0
        llm_retry_backoff_seconds = 0.0
        llm_circuit_breaker_fail_threshold = 3
        llm_circuit_breaker_open_seconds = 10.0

    gw_mod.settings = _S()

    try:
        result = await gw.chat(messages=[{"role": "user", "content": "hi"}])
        assert result.provider == "openrouter"
        assert flaky.calls == 2
    finally:
        gw_mod.settings = old_settings


@pytest.mark.asyncio
async def test_gateway_circuit_open_skips_provider():
    gw = object.__new__(LLMGateway)
    gw.backends = {"openrouter": _FakeBackendFail(), "gemini": _FakeBackendOk()}

    from trendpulse.core.llm import gateway as gw_mod

    old_settings = gw_mod.settings

    class _S:
        default_provider = "openrouter"
        fallback_provider = "gemini"
        default_model = "openrouter/auto"
        llm_max_retries = 0
        llm_request_timeout_seconds = 1.0
        llm_retry_backoff_seconds = 0.0
        llm_circuit_breaker_fail_threshold = 1
        llm_circuit_breaker_open_seconds = 60.0

    gw_mod.settings = _S()

    try:
        first = await gw.chat(messages=[{"role": "user", "content": "hi"}])
        assert first.provider == "gemini"

        second = await gw.chat(messages=[{"role": "user", "content": "hi"}])
        assert second.provider == "gemini"
    finally:
        gw_mod.settings = old_settings


@pytest.mark.asyncio
async def test_gateway_timeout_fallback():
    gw = object.__new__(LLMGateway)
    gw.backends = {"openrouter": _FakeBackendTimeout(), "gemini": _FakeBackendOk()}

    from trendpulse.core.llm import gateway as gw_mod

    old_settings = gw_mod.settings

    class _S:
        default_provider = "openrouter"
        fallback_provider = "gemini"
        default_model = "openrouter/auto"
        llm_max_retries = 0
        llm_request_timeout_seconds = 0.01
        llm_retry_backoff_seconds = 0.0
        llm_circuit_breaker_fail_threshold = 3
        llm_circuit_breaker_open_seconds = 10.0

    gw_mod.settings = _S()

    try:
        result = await gw.chat(messages=[{"role": "user", "content": "hi"}])
        assert result.provider == "gemini"
    finally:
        gw_mod.settings = old_settings
