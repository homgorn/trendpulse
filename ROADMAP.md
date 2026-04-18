# ROADMAP.md — TrendPulse Development Roadmap

## Current Status: v0.2.1 — Production Ready

## Completed ✅

### v0.1.0 — MVP Core
- [x] LLM Gateway with OpenRouter + Gemini adapters
- [x] Model routing policy (reasoning, creative, balanced)
- [x] CLI generate command
- [x] Basic tests

### v0.2.0 — Production Hardening
- [x] FastAPI lifespan pattern
- [x] CORS middleware
- [x] Security headers
- [x] Global exception handler
- [x] Rate limiter (in-memory)
- [x] Improved metrics with per-provider tracking
- [x] JSON parsing robustness
- [x] Multi-stage Dockerfile with uv
- [x] Docker Compose stack
- [x] Kubernetes manifests
- [x] Monitoring configs (OTel, Prometheus)
- [x] CI/CD pipelines
- [x] SEO landing page
- [x] Makefile for dev commands
- [x] AGENTS.md, CONTEXT_MAP.md, SECURITY.md, CHANGELOG.md

### v0.2.1 — Observability & Testing
- [x] OpenTelemetry tracing integration
- [x] Structured JSON logging support
- [x] Database module (SQLAlchemy async, PostgreSQL-ready)
- [x] Locust load test suite
- [x] CSV/JSON logs support
- [x] HTTP client logging suppression

---

## In Progress (v0.3.0)

### Core Features
- [ ] API Key authentication (per-user)
- [ ] Request validation & sanitization
- [ ] Persistent metrics storage (PostgreSQL)

### Infrastructure
- [ ] PostgreSQL integration for metadata (using database.py)
- [ ] Valkey integration for rate limiting
- [ ] Vector DB integration (Qdrant) for RAG

### Observability
- [x] OpenTelemetry tracing (basic integration done)
- [x] Structured logging (JSON support added)
- [ ] Distributed tracing (production ready)

---

## Planned (v0.4.0 — Growth)

### Features
- [ ] User management & authentication
- [ ] API key management dashboard
- [ ] Request history & analytics
- [ ] Webhooks for notifications

### Providers
- [ ] DeepSeek adapter (reasoning models)
- [ ] OpenAI adapter (GPT models)
- [ ] Claude adapter (Anthropic)
- [ ] Together/Fireworks adapters

---

## Future (v1.0.0 — Enterprise)

### Core
- [ ] Multi-tenant architecture
- [ ] Rate limiting per user
- [ ] Quota management
- [ ] Billing integration (Stripe)

### Data
- [ ] Trend ingestion connectors (TikTok, crypto)
- [ ] Vector brain for semantic search
- [ ] RAG pipeline for context-aware generation

### Integration
- [ ] MCP Server exposure
- [ ] Jira/Linear integration
- [ ] Slack notifications

---

## Tech Debt

- [ ] Replace in-memory metrics with persistent storage
- [ ] Replace in-memory rate limiter with Valkey-backed
- [x] Add integration tests with testcontainers (foundation ready)
- [x] Performance testing (Locust test added)
- [ ] Security audit (OWASP)

---

## Dependencies & External APIs

### Required
- OpenRouter API (https://openrouter.ai)
- Google Gemini API (https://ai.google.dev)

### Optional (for future)
- DeepSeek API
- OpenAI API
- Anthropic API
- Qdrant (vector DB)
- PostgreSQL (managed)
- Valkey (managed)

---

## Quick Start for Development

```bash
# Install dependencies
make install

# Run tests
make test

# Run locally
make run

# Build Docker
make docker-build

# Run with Docker Compose
make docker-up
```

## Environment Variables

Required for production:
- `OPENROUTER_API_KEY` or `GEMINI_API_KEY`

Optional:
- `DATABASE_URL` - PostgreSQL connection (for v0.3.0)
- `VALKEY_URL` - Valkey/Redis for caching (for v0.3.0)
- `OTEL_ENABLED=true` - Enable OpenTelemetry
- `OTEL_ENDPOINT` - OTel collector endpoint