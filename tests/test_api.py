from fastapi.testclient import TestClient

from trendpulse import api as api_mod
from trendpulse.errors import ProviderError, ProviderTimeoutError


class _FakeService:
    async def generate(self, req, trace_id=None):
        from trendpulse.schemas import GenerateResponse

        return GenerateResponse(
            idea="Idea",
            audience="Audience",
            monetization="Subs",
            risks=["risk1"],
            sources=["src1"],
            provider="gemini",
            model="gemini-2.0-flash",
            profile="creative",
        )


class _FakeServiceTimeout:
    async def generate(self, req, trace_id=None):
        raise ProviderTimeoutError("provider timeout test")


class _FakeServiceMalformed:
    async def generate(self, req, trace_id=None):
        raise ProviderError("malformed response test")


class _FakeServiceFallbackChain:
    async def generate(self, req, trace_id=None):
        from trendpulse.schemas import GenerateResponse

        return GenerateResponse(
            idea="Fallback Idea",
            audience="Fallback Audience",
            monetization="Fallback Subs",
            risks=[],
            sources=[],
            provider="gemini",
            model="gemini-2.0-flash",
            profile="analysis",
        )


def test_health():
    client = TestClient(api_mod.app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_ready_endpoint_default_not_ready(monkeypatch):
    class _FakeGateway:
        backends = {}

    monkeypatch.setattr(api_mod, "LLMGateway", lambda: _FakeGateway())

    client = TestClient(api_mod.app)
    r = client.get("/ready")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] in {"ready", "not_ready"}


def test_metrics_endpoint():
    client = TestClient(api_mod.app)
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "trendpulse_requests_total" in r.text
    assert "trendpulse_llm_latency_ms_sum" in r.text


def test_generate_success(monkeypatch):
    def _service_factory(*args, **kwargs):
        return _FakeService()

    monkeypatch.setattr(api_mod, "TrendPulseService", _service_factory)
    monkeypatch.setattr(api_mod, "LLMGateway", lambda: object())

    client = TestClient(api_mod.app)
    payload = {"theme": "ai tools", "platform": "tiktok"}
    r = client.post("/v1/generate", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["idea"] == "Idea"


def test_generate_validation_error():
    client = TestClient(api_mod.app)
    payload = {"theme": "a", "platform": "tiktok"}
    r = client.post("/v1/generate", json=payload)
    assert r.status_code == 422


def test_generate_provider_timeout_error(monkeypatch):
    def _service_factory(*args, **kwargs):
        return _FakeServiceTimeout()

    monkeypatch.setattr(api_mod, "TrendPulseService", _service_factory)
    monkeypatch.setattr(api_mod, "LLMGateway", lambda: object())

    client = TestClient(api_mod.app)
    payload = {"theme": "ai tools", "platform": "tiktok"}
    r = client.post("/v1/generate", json=payload)
    assert r.status_code == 400
    body = r.json()
    assert body["code"] == "PROVIDER_TIMEOUT"


def test_generate_malformed_provider_error(monkeypatch):
    def _service_factory(*args, **kwargs):
        return _FakeServiceMalformed()

    monkeypatch.setattr(api_mod, "TrendPulseService", _service_factory)
    monkeypatch.setattr(api_mod, "LLMGateway", lambda: object())

    client = TestClient(api_mod.app)
    payload = {"theme": "ai tools", "platform": "tiktok"}
    r = client.post("/v1/generate", json=payload)
    assert r.status_code == 400
    body = r.json()
    assert body["code"] == "PROVIDER_ERROR"


def test_generate_fallback_chain_behavior(monkeypatch):
    def _service_factory(*args, **kwargs):
        return _FakeServiceFallbackChain()

    monkeypatch.setattr(api_mod, "TrendPulseService", _service_factory)
    monkeypatch.setattr(api_mod, "LLMGateway", lambda: object())

    client = TestClient(api_mod.app)
    payload = {"theme": "ai tools", "platform": "tiktok"}
    r = client.post("/v1/generate", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["provider"] == "gemini"
    assert body["idea"] == "Fallback Idea"
