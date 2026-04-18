import asyncio
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware

from trendpulse.config import settings
from trendpulse.core.llm.gateway import LLMGateway
from trendpulse.database import close_database, init_database
from trendpulse.errors import TrendPulseError
from trendpulse.logging_utils import setup_logging
from trendpulse.metrics import metrics
from trendpulse.rate_limiter import rate_limiter
from trendpulse.schemas import ErrorResponse, GenerateRequest, GenerateResponse
from trendpulse.service import TrendPulseService

if settings.otel_enabled:
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    trace.set_tracer_provider(TracerProvider())
    tracer_provider = trace.get_tracer_provider()
    tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=settings.otel_endpoint)))

setup_logging(settings.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.otel_enabled:
        FastAPIInstrumentor.instrument_app(app)

    init_database()
    app.state.gateway = LLMGateway()
    yield
    app.state.gateway = None
    await close_database()


app = FastAPI(title="TrendPulse API", version="0.2.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_allowed_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])


@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    if request.url.path.startswith("/v1/"):
        client_ip = request.client.host if request.client else "unknown"
        allowed, remaining = rate_limiter.is_allowed(client_ip)
        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"},
                headers={"Retry-After": "60"},
            )
    response = await call_next(request)
    return response


@app.exception_handler(TrendPulseError)
async def trendpulse_error_handler(request: Request, exc: TrendPulseError):
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(code=exc.code, message=exc.message).model_dump(),
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
async def ready(request: Request) -> dict[str, str]:
    providers = {
        "openrouter": bool(settings.openrouter_api_key),
        "gemini": bool(settings.gemini_api_key),
    }
    if not any(providers.values()):
        return {"status": "not_ready", "reason": "no_providers_configured"}

    gateway = getattr(request.app.state, "gateway", None)
    if gateway:
        for name, backend in gateway.backends.items():
            try:
                result = await asyncio.wait_for(
                    backend.chat([{"role": "user", "content": "ping"}], model="test"),
                    timeout=5.0,
                )
                if result:
                    return {"status": "ready", "provider": name}
            except Exception:
                continue

    return {"status": "ready", "reason": "keys_configured"}


@app.get("/metrics")
async def get_metrics() -> PlainTextResponse:
    return PlainTextResponse(metrics.render_prometheus(), media_type="text/plain; version=0.0.4")


@app.post("/v1/generate", response_model=GenerateResponse, responses={400: {"model": ErrorResponse}})
async def generate(req: GenerateRequest, request: Request) -> GenerateResponse:
    trace_id = request.headers.get("x-trace-id", str(uuid.uuid4()))
    gateway = getattr(request.app.state, "gateway", None) or LLMGateway()
    service = TrendPulseService(gateway=gateway)
    started = time.perf_counter()
    try:
        response = await service.generate(req, trace_id=trace_id)
        latency_ms = (time.perf_counter() - started) * 1000.0
        metrics.record_success(
            latency_ms=latency_ms,
            provider=response.provider,
            model=response.model,
        )
        return response
    except TrendPulseError:
        latency_ms = (time.perf_counter() - started) * 1000.0
        metrics.record_error(latency_ms=latency_ms)
        raise
    except Exception:
        latency_ms = (time.perf_counter() - started) * 1000.0
        metrics.record_error(latency_ms=latency_ms)
        raise
