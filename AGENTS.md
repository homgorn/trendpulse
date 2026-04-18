# AGENTS.md — AI Agent Context File

## Project Overview

TrendPulse is an AI-driven market intelligence and content generation platform for gaming studios. It monitors trends across multiple industries and generates game concepts using multi-provider LLM routing.

## Architecture

```
trendpulse/
├── src/trendpulse/
│   ├── api.py              # FastAPI application with lifespan
│   ├── config.py           # Pydantic Settings (env vars)
│   ├── schemas.py          # Pydantic models (request/response)
│   ├── service.py          # Business logic (TrendPulseService)
│   ├── errors.py           # Domain exceptions
│   ├── metrics.py          # Prometheus metrics registry
│   ├── rate_limiter.py     # In-memory rate limiter
│   ├── logging_utils.py    # Logging with trace_id support
│   ├── cli.py              # Typer CLI
│   ├── core/llm/
│   │   ├── gateway.py      # LLM Gateway (fallback, circuit breaker)
│   │   ├── routing.py      # Model routing policy
│   │   └── backends.py    # Abstract LLMBackend
│   └── adapters/
│       ├── openrouter_backend.py
│       └── gemini_backend.py
├── api.py                  # Entry point (uvicorn)
├── k8s/                    # Kubernetes manifests
├── monitoring/             # OTel, Prometheus configs
└── tests/                  # Test suite
```

## AI-IDE Integration

- **Claude Code**: Use CLAUDE.md in project root
- **Cursor**: Configure .cursorrules with this architecture
- **Windsurf**: Add .windsurfrules

## Vibe Coding Workflow

1. AGENTS.md is read FIRST before any code
2. CONTEXT_MAP.md provides visual system map
3. All changes pass through `ruff check` + `pytest`
4. New files are added to CONTEXT_MAP.md
5. Use `make` commands for common operations

## Key Files

- `src/trendpulse/api.py` - FastAPI app, routes, middleware
- `src/trendpulse/core/llm/gateway.py` - Core LLM routing logic
- `src/trendpulse/service.py` - Business logic layer
- `pyproject.toml` - Project configuration

## Commands

```bash
make install   # Install deps
make test      # Run tests
make lint      # Lint code
make run       # Run locally
```
