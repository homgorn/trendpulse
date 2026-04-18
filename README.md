---
title: TrendPulse — AI Market Intelligence for Gaming Studios
description: TrendPulse is an open-source AI platform for game studios to discover market trends and generate game concepts. Features multi-provider LLM routing, RAG, circuit breaker, production-ready.
keywords: game development, market intelligence, AI gaming, trend analysis, game design, LLM, GDD generator, gaming trends, AI platform
author: TrendPulse Team
robots: index, follow
og:title: TrendPulse — AI for Gaming Market Intelligence
og:description: Turn market noise into successful games with AI-driven trend detection and game concept generation.
og:type: website
og:url: https://homgorn.github.io/trendpulse/
og:locale: en_US
og:image: https://homgorn.github.io/trendpulse/og-image.svg
twitter:card: summary_large_image
twitter:title: TrendPulse — AI for Gaming Market Intelligence
twitter:description: Turn market noise into successful games
---

# TrendPulse — AI Market Intelligence for Gaming

<p align="center">
  <a href="https://pypi.org/project/trendpulse/"><img src="https://img.shields.io/badge/version-0.2.0-blue.svg" alt="Version"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.11%2B-green.svg" alt="Python"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License"></a>
  <a href="https://github.com/homgorn/trendpulse/actions"><img src="https://img.shields.io/badge/status-Production%20Ready-brightgreen.svg" alt="Status"></a>
</p>

**TrendPulse** is an open-source AI platform for game studios to discover market trends and generate game concepts. Features multi-provider LLM routing (OpenRouter, Gemini), RAG-based retrieval, circuit breaker, rate limiting.

| [English](README.md) | [Русский](README-RU.md) | [Docs](docs/) | [Investors](investors/) | [GitHub](https://github.com/homgorn/trendpulse) |

## Quick Start

```bash
pip install trendpulse
export OPENROUTER_API_KEY=your_key
trendpulse generate --theme "battle royale" --platform mobile
```

Or with Docker:

```bash
docker run -p 8000:8000 -e OPENROUTER_API_KEY=your_key ghcr.io/homgorn/trendpulse:latest
```

---

## Features

| Feature | Description |
|---------|-------------|
| **REST API** | FastAPI-based HTTP API with `/health`, `/ready`, `/metrics`, `/v1/generate` endpoints |
| **CLI** | Command-line interface for programmatic access |
| **Multi-Provider LLM** | OpenRouter (300+ models) + Google Gemini with automatic fallback |
| **Circuit Breaker** | Configurable failure threshold and recovery timeout |
| **Rate Limiting** | In-memory rate limiter with configurable limits |
| **Observability** | Prometheus metrics, OpenTelemetry tracing support |
| **Error Handling** | Structured error codes with proper HTTP status mapping |

---

## Architecture

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   REST API   │--->│   Service   │--->│  LLM Gateway│
│   (FastAPI)  │    │  (Business  │    │ (Routing +   │
└──────────────┘    │   Logic)     │    │  Fallback)   │
                    └──────────────┘    └──────┬───────┘
                                           │
         ┌────────────────────────────────────┼────────────┐
         │         Adapters Layer              │
         │  ┌──────────────┐    ┌───────────┐│
         │  │ OpenRouter   │    │   Gemini  ││
         │  └──────────────┘    └───────────┘│
         └────────────────────────────────────┘
```

**Core**: API (`api.py`), Service (`service.py`), Gateway (`gateway.py`), Adapters (OpenRouter, Gemini)

---

## Install
- pip or uv package manager
- API keys for at least one LLM provider

### Installation

```bash
# Clone repository
git clone https://github.com/homgorn/trendpulse.git
cd trendpulse

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/macOS)
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"
```

### Environment Configuration

Create a `.env` file:

```env
# LLM Providers (at least one required)
OPENROUTER_API_KEY=sk-or-...
GEMINI_API_KEY=...

# Optional Configuration
DEFAULT_PROVIDER=openrouter
FALLBACK_PROVIDER=gemini
LOG_LEVEL=INFO

# Rate Limiting
RATE_LIMIT_REQUESTS=30
RATE_LIMIT_WINDOW_SECONDS=60

# Observability
OTEL_ENABLED=false
OTEL_ENDPOINT=http://localhost:4317
```

### Run Locally

```bash
uvicorn trendpulse.api:app --host 127.0.0.1 --port 8100 --reload
```

API available at: `http://127.0.0.1:8100`

---

## API Reference

### Endpoints

#### GET /health

Health check — always returns `{"status": "ok"}`

```bash
curl http://127.0.0.1:8100/health
```

#### GET /ready

Readiness check — verifies LLM provider configuration

```bash
curl http://127.0.0.1:8100/ready
```

#### GET /metrics

Prometheus metrics endpoint

```bash
curl http://127.0.0.1:8100/metrics
```

#### POST /v1/generate

Generate game concept based on market trends

**Request Body:**

```json
{
  "theme": "ai tools",
  "platform": "tiktok",
  "region": "global",
  "budget_mode": "balanced",
  "task_type": "creative"
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `theme` | string | Yes | Theme or niche for idea generation (2-500 chars) |
| `platform` | string | Yes | Target platform (tiktok, mobile, steam, console) |
| `region` | string | No | Target region (default: "global") |
| `budget_mode` | string | No | "balanced" or "low_cost" (default: "balanced") |
| `task_type` | string | No | "creative", "analysis", or "reasoning" (default: "creative") |

**Response:**

```json
{
  "idea": "AI-powered short-form video creator...",
  "audience": "Gen Z content creators...",
  "monetization": "Freemium with premium features...",
  "risks": ["Market saturation", "Platform dependency"],
  "sources": ["TikTok trends", "Product Hunt data"],
  "provider": "openrouter",
  "model": "anthropic/claude-3.5-sonnet",
  "profile": "creative"
}
```

**Error Responses:**

| Status Code | Description |
|-------------|-------------|
| 400 | Bad Request — validation error |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

---

## CLI Usage

### Generate Command (Recommended)

```bash
trendpulse generate \
  --theme "ai tools" \
  --platform "tiktok" \
  --region "global" \
  --budget-mode balanced \
  --task-type creative
```

### Legacy Mode

```bash
trendpulse \
  --theme "ai tools" \
  --platform "tiktok" \
  --region "global" \
  --budget-mode balanced \
  --task-type creative
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | — | OpenRouter API key |
| `GEMINI_API_KEY` | — | Google Gemini API key |
| `DEFAULT_PROVIDER` | openrouter | Primary LLM provider |
| `FALLBACK_PROVIDER` | gemini | Fallback provider |
| `DEFAULT_MODEL` | openrouter/auto | Default model |
| `LLM_REQUEST_TIMEOUT_SECONDS` | 30 | Request timeout |
| `LLM_MAX_RETRIES` | 1 | Maximum retries |
| `LLM_RETRY_BACKOFF_SECONDS` | 0.25 | Initial backoff (exponential) |
| `LLM_CIRCUIT_BREAKER_FAIL_THRESHOLD` | 3 | Failures before circuit opens |
| `LLM_CIRCUIT_BREAKER_OPEN_SECONDS` | 20 | Circuit open duration |
| `RATE_LIMIT_REQUESTS` | 30 | Requests per window |
| `RATE_LIMIT_WINDOW_SECONDS` | 60 | Window duration in seconds |
| `OTEL_ENABLED` | false | Enable OpenTelemetry |
| `OTEL_ENDPOINT` | localhost:4317 | OTel collector endpoint |

---

## Deployment

### Docker

```bash
# Build image
docker build -t trendpulse:latest .

# Run container
docker run --rm -p 8100:8100 -v .env:/app/.env trendpulse:latest
```

### Docker Compose

```bash
docker compose up --build
```

### Kubernetes

See `k8s/` directory for manifests:

```bash
kubectl apply -f k8s/
```

---

## Monitoring

### Prometheus Metrics

Available at `/metrics` endpoint:

```
trendpulse_requests_total
trendpulse_requests_success_total
trendpulse_requests_error_total
trendpulse_llm_latency_ms_sum
trendpulse_llm_latency_ms_count
trendpulse_provider_{provider}_requests_total
trendpulse_provider_{provider}_latency_ms_sum
trendpulse_provider_{provider}_cost_usd_total
```

### Grafana Dashboard

Import `monitoring/grafana-dashboard.json` for pre-built dashboards.

### OpenTelemetry

Configure `OTEL_ENABLED=true` and `OTEL_ENDPOINT` for distributed tracing.

---

## Running Tests

```bash
# Run all tests
pytest -v

# Run specific tests
pytest tests/test_gateway.py -v
pytest tests/test_routing.py -v

# With coverage
pytest --cov=trendpulse tests/
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Run linting: `ruff check src/`
5. Submit a pull request

---

## License

MIT License — see [LICENSE](LICENSE) file.

---

## Resources

- [Documentation](docs/)
- [API Schema](contracts/)
- [Product Requirements](prd/)
- [Changelog](CHANGELOG.md)
- [Roadmap](ROADMAP.md)

---

<p align="center">Built with ❤️ for game studios worldwide</p>