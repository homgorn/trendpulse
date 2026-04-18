# CONTEXT_MAP.md — System Architecture Map

## Overview

TrendPulse is an AI-driven market intelligence platform that converts market trends into game concepts using multi-provider LLM routing.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTS                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   CLI       │  │  REST API   │  │   Web UI (Future)       │  │
│  │ (Typer)     │  │ (FastAPI)   │  │   (Next.js)             │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        API LAYER                                 │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  FastAPI Application (api.py)                              │  │
│  │  • /health, /ready, /metrics                               │  │
│  │  • /v1/generate                                            │  │
│  │  • Middleware: CORS, Security Headers, Rate Limiting       │  │
│  │  • Error Handling, Lifespan Management                    │  │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                         │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  TrendPulseService (service.py)                           │  │
│  │  • Prompt Template Generation                              │  │
│  │  • JSON Parsing & Validation                               │  │
│  │  • Response Mapping                                        │  │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     LLM GATEWAY LAYER                            │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  LLMGateway (gateway.py)                                  │  │
│  │  • Retry Logic (configurable)                             │  │
│  │  • Circuit Breaker Pattern                                │  │
│  │  • Provider Fallback Chain                                │  │
│  │  • Model Routing (routing.py)                             │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ OpenRouter   │  │   Gemini     │  │   Future    │          │
│  │   Backend    │  │   Backend    │  │   Backends  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     INFRASTRUCTURE LAYER                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  PostgreSQL  │  │   Valkey     │  │   LLM API    │          │
│  │  (Future)    │  │  (Future)   │  │  (External)  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

1. **Request Flow**: CLI/API → FastAPI Middleware → Service → Gateway → Provider → Response
2. **Error Flow**: Provider Error → Circuit Breaker → Fallback Provider → Error Response
3. **Metrics Flow**: Request → Metrics Registry → Prometheus Endpoint

## API Endpoints

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/health` | GET | Health check | No |
| `/ready` | GET | Readiness check | No |
| `/metrics` | GET | Prometheus metrics | No |
| `/v1/generate` | POST | Generate game concept | No (MVP) |

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENROUTER_API_KEY` | Yes* | - | OpenRouter API key |
| `GEMINI_API_KEY` | Yes* | - | Google Gemini API key |
| `DEFAULT_PROVIDER` | No | openrouter | Primary LLM provider |
| `FALLBACK_PROVIDER` | No | gemini | Fallback LLM provider |
| `CORS_ALLOWED_ORIGINS` | No | localhost:3000 | Allowed CORS origins |

*At least one provider API key required

## Module Dependencies

```
api.py
├── config.py (settings)
├── logging_utils.py
├── metrics.py
├── rate_limiter.py
├── schemas.py
├── errors.py
├── service.py
│   └── core/llm/gateway.py
│       ├── core/llm/routing.py
│       └── adapters/
│           ├── openrouter_backend.py
│           └── gemini_backend.py
└── cli.py
```

## Key Design Decisions

1. **Lifespan Pattern**: Async context manager for resource initialization/cleanup
2. **Provider Fallback**: Automatic switch on failure with circuit breaker
3. **Metrics**: Thread-safe in-memory registry with Prometheus format
4. **Rate Limiting**: Sliding window algorithm, IP-based (MVP)
5. **Security Headers**: X-Content-Type-Options, X-Frame-Options, CSP

## Future Enhancements

- PostgreSQL for persistent storage
- Valkey/Redis for caching and rate limiting
- Vector DB for trend embeddings
- User authentication (API keys, JWT)
- Rate limiting per user
- MCP Server exposure