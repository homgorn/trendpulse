# CLAUDE.md — Claude Code AI-IDE Context

## Project Overview

TrendPulse — AI-driven market intelligence & game concept generator for gaming studios. Multi-provider LLM routing (OpenRouter, Gemini), RAG-based retrieval, circuit breaker, rate limiting.

## Architecture

```
trendpulse/
├── src/trendpulse/
│   ├── api.py              # FastAPI routes, middleware
│   ├── service.py         # TrendPulseService business logic
│   ├── config.py         # Pydantic Settings
│   ├── schemas.py        # Request/Response models
│   ├── errors.py        # Domain exceptions
│   ├── core/llm/
│   │   ├── gateway.py   # LLM Gateway (fallback, circuit breaker)
│   │   ├── routing.py   # Model routing policy
│   │   └── backends.py # Abstract LLMBackend
│   └── adapters/
│       ├── openrouter_backend.py
│       └── gemini_backend.py
├── tests/               # Test suite
├── monitoring/         # Prometheus, Grafana, OTel
└── k8s/              # Kubernetes manifests
```

## Commands

```bash
make install   # Install deps
make test     # Run tests
make lint     # Lint code
make run      # Run locally
```

## Key Files

- `src/trendpulse/api.py` — FastAPI app, routes, lifespan
- `src/trendpulse/service.py` — Business logic
- `src/trendpulse/core/llm/gateway.py` — LLM routing + circuit breaker
- `pyproject.toml` — Project config

## Workflow

1. Read AGENTS.md first
2. All changes pass `ruff check` + `pytest`
3. New files add to CONTEXT_MAP.md
4. Use `make` commands

## Important

- No hardcoded secrets in code
- Use Pydantic for validation
- All async endpoints
- Circuit breaker pattern for LLM fallbacks