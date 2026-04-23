import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse

from trendpulse.config import settings
from trendpulse.core.llm.gateway import LLMGateway
from trendpulse.errors import TrendPulseError
from trendpulse.logging_utils import setup_logging
from trendpulse.metrics import metrics
from trendpulse.schemas import ErrorResponse, GenerateRequest, GenerateResponse
from trendpulse.service import TrendPulseService

setup_logging(settings.log_level)
app = FastAPI(title="TrendPulse API", version="0.1.0")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
async def ready() -> dict[str, str]:
    providers = {
        "openrouter": bool(settings.openrouter_api_key),
        "gemini": bool(settings.gemini_api_key),
    }
    if any(providers.values()):
        return {"status": "ready"}
    return {"status": "not_ready"}


@app.get("/metrics")
async def get_metrics() -> PlainTextResponse:
    return PlainTextResponse(metrics.render_prometheus(), media_type="text/plain; version=0.0.4")


@app.post("/v1/generate", response_model=GenerateResponse, responses={400: {"model": ErrorResponse}})
async def generate(req: GenerateRequest, request: Request) -> GenerateResponse:
    trace_id = request.headers.get("x-trace-id", str(uuid.uuid4()))
    service = TrendPulseService(gateway=LLMGateway())
    started = time.perf_counter()
    try:
        response = await service.generate(req, trace_id=trace_id)
        latency_ms = (time.perf_counter() - started) * 1000.0
        metrics.record_success(latency_ms=latency_ms)
        return response
    except Exception:
        latency_ms = (time.perf_counter() - started) * 1000.0
        metrics.record_error(latency_ms=latency_ms)
        raise


@app.exception_handler(TrendPulseError)
async def trendpulse_error_handler(_: Request, exc: TrendPulseError):
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(code=exc.code, message=exc.message).model_dump(),
    )
