# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2026-04-08

### Added
- OpenTelemetry tracing integration (auto-instrumentation for FastAPI)
- Structured JSON logging support (optional, via LOG_JSON=true)
- Database module (SQLAlchemy async, PostgreSQL-ready)
- Locust load test suite (`tests/load_test.py`)
- Database config options (`DATABASE_URL`, `database_pool_size`, `valkey_url`)
- HTTP client logging suppression (httpx, httpcore)
- USAGE.md documentation

### Changed
- Enhanced logging with JSONFormatter option
- Suppressed verbose HTTP client logs in production

## [0.2.0] - 2026-04-08

### Added
- FastAPI lifespan pattern for resource management
- CORS middleware with configurable origins
- Security headers (X-Content-Type-Options, X-Frame-Options, CSP, HSTS)
- Global exception handler
- In-memory rate limiter (sliding window algorithm)
- Per-provider metrics (latency, errors, tokens, cost)
- JSON parsing robustness (regex cleanup, nested extraction)
- Input validation with field constraints (max length, patterns)
- Multi-stage Dockerfile with uv
- Docker Compose with full stack (API, PostgreSQL, Valkey, Nginx, OTel, Prometheus, Grafana)
- Kubernetes manifests (Deployment, Service, Ingress, HPA, ConfigMap, Secrets)
- Nginx reverse proxy with rate limiting
- OpenTelemetry collector configuration
- Prometheus scraping configuration
- Alertmanager configuration
- GitHub Actions CI pipeline (ruff, pytest, security scan)
- GitHub Actions CD pipeline (Docker build/push, K8s deploy)
- GitHub Actions Security pipeline (dependabot, codeql, trivy)
- SEO landing page with JSON-LD schemas
- Makefile for dev commands
- AGENTS.md for AI-IDE context
- CONTEXT_MAP.md for system architecture
- ROADMAP.md for development plan
- SECURITY.md for security policy
- .env.example template
- .gitignore, .dockerignore, .editorconfig
- .pre-commit-config.yaml

### Changed
- Upgraded pyproject.toml to uv standard (Python 3.12+, ruff, locust)
- Improved metrics with provider-level tracking
- Enhanced routing with budget_mode constraints
- Better error handling in service layer

### Fixed
- JSON parsing robustness for markdown code blocks
- Input validation constraints

## [0.1.0] - 2026-03-01

### Added
- LLM Gateway with OpenRouter + Gemini adapters
- Model routing policy (reasoning, creative, balanced)
- Circuit breaker pattern
- Retry logic with configurable backoff
- Provider fallback chain
- CLI generate command (Typer)
- REST API endpoints (/health, /ready, /metrics, /v1/generate)
- Basic Prometheus metrics
- Logging with trace_id support
- Docker support
- Initial test suite

### Fixed
- Gateway initialization without providers
- Timeout handling

---

## Upgrade Notes

### 0.1.x → 0.2.0
- Add required environment variables: `CORS_ALLOWED_ORIGINS`, `RATE_LIMIT_REQUESTS`, `RATE_LIMIT_WINDOW_SECONDS`
- Ensure at least one LLM provider API key is configured
- Update to Python 3.12+ for best compatibility