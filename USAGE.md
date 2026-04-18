# USAGE.md — TrendPulse API Usage Guide

## Quick Start

### Local Development

```bash
# Clone and setup
git clone https://github.com/homgorn/trendpulse.git
cd trendpulse

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Copy and configure .env
cp .env.example .env
# Edit .env with your API keys

# Run the API
uvicorn api:app --reload

# Or use CLI
trendpulse generate --theme "ai tools" --platform "tiktok"
```

## API Endpoints

### Health Check

```bash
curl http://127.0.0.1:8100/health
```

Response:
```json
{"status": "ok"}
```

### Readiness Check

```bash
curl http://127.0.0.1:8100/ready
```

Response:
```json
{"status": "ready"}  # or "not_ready" if no API keys configured
```

### Metrics (Prometheus)

```bash
curl http://127.0.0.1:8100/metrics
```

### Generate Game Idea

```bash
curl -X POST http://127.0.0.1:8100/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "theme": "ai tools",
    "platform": "tiktok",
    "region": "global",
    "budget_mode": "balanced",
    "task_type": "creative"
  }'
```

Response:
```json
{
  "idea": "...",
  "audience": "...",
  "monetization": "...",
  "risks": [...],
  "sources": [...],
  "provider": "openrouter",
  "model": "qwen/qwen-2.5-72b-instruct",
  "profile": "creative"
}
```

## CLI Usage

### Generate Command

```bash
# Basic
trendpulse generate --theme "crypto gaming" --platform "mobile"

# Full options
trendpulse generate \
  --theme "ai tools" \
  --platform "tiktok" \
  --region "global" \
  --budget-mode "balanced" \
  --task-type "creative"
```

### Options

| Flag | Description | Default |
|------|--------------|---------|
| `--theme` | Theme/niche for idea | Required |
| `--platform` | Target platform | tiktok |
| `--region` | Target region | global |
| `--budget-mode` | Cost optimization | balanced |
| `--task-type` | Generation type | creative |

### Legacy Mode

```bash
trendpulse --theme "crypto" --platform "mobile"
```

## Configuration

### Environment Variables

```bash
# Required (at least one)
OPENROUTER_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here

# Optional
DEFAULT_PROVIDER=openrouter
FALLBACK_PROVIDER=gemini
DEFAULT_MODEL=openrouter/auto

# Performance tuning
LLM_REQUEST_TIMEOUT_SECONDS=30
LLM_MAX_RETRIES=1
LLM_RETRY_BACKOFF_SECONDS=0.25
LLM_CIRCUIT_BREAKER_FAIL_THRESHOLD=3
LLM_CIRCUIT_BREAKER_OPEN_SECONDS=20

# Security
CORS_ALLOWED_ORIGINS=http://localhost:3000
RATE_LIMIT_REQUESTS=30
RATE_LIMIT_WINDOW_SECONDS=60
```

## Docker

### Build and Run

```bash
# Build image
docker build -t trendpulse:latest .

# Run container
docker run -p 8100:8100 -e OPENROUTER_API_KEY=your_key trendpulse:latest
```

### Docker Compose

```bash
# Start all services
docker compose up --build

# Run in background
docker compose up -d
```

## Troubleshooting

### API Key Not Working

1. Check `.env` file exists and has valid keys
2. Verify keys are correct format
3. Check `/ready` endpoint shows "ready"

### Rate Limiting

If you get 429 errors:
- Wait 60 seconds before retrying
- Adjust `RATE_LIMIT_REQUESTS` in `.env`
- Check `/metrics` for request counts

### Timeout Errors

If requests timeout:
- Increase `LLM_REQUEST_TIMEOUT_SECONDS`
- Check network connectivity
- Try different `DEFAULT_PROVIDER`

### Circuit Breaker

If all providers fail:
- Check API key validity
- Wait for circuit to reset (default 20s)
- Check logs for specific errors

## Performance

### Monitoring

```bash
# View metrics
curl http://127.0.0.1:8100/metrics

# Prometheus format - import to Grafana
```

### Load Testing

```bash
# Run Locust load test
locust -f tests/load_test.py --host=http://127.0.0.1:8100

# Web UI at http://localhost:8089
```

## API Reference

### GenerateRequest

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| theme | string | Yes | Theme/niche (min 2 chars) |
| platform | string | Yes | Target platform |
| region | string | No | Target region (default: global) |
| budget_mode | string | No | balanced or low_cost |
| task_type | string | No | creative, analysis, or reasoning |

### GenerateResponse

| Field | Type | Description |
|-------|------|-------------|
| idea | string | Generated game idea |
| audience | string | Target audience |
| monetization | string | Monetization strategy |
| risks | array | List of risks |
| sources | array | Data sources used |
| provider | string | LLM provider used |
| model | string | Model used |
| profile | string | Task profile used |

### ErrorResponse

| Field | Type | Description |
|-------|------|-------------|
| code | string | Error code |
| message | string | Error message |

## Support

- GitHub Issues: https://github.com/homgorn/trendpulse/issues
- Documentation: https://trendpulse.com/docs