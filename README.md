# TrendPulse

TrendPulse — FastAPI/CLI сервис для генерации продуктовых идей с маршрутизацией по LLM-профилям, fallback между провайдерами и базовой операционной наблюдаемостью.

## Features

- HTTP API:
  - `GET /health`
  - `GET /ready`
  - `GET /metrics` (Prometheus text format)
  - `POST /v1/generate`
- CLI:
  - Multi-command: `trendpulse generate ...`
  - Legacy-compatible mode: `trendpulse --theme ... --platform ...`
- Resilience:
  - timeout / retries / circuit breaker (config-driven)
  - provider fallback
- Tests:
  - gateway + api + cli + routing

## Requirements

- Python 3.11+
- pip

## Local setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -e ".[dev]"
```

## Run API locally

```bash
uvicorn trendpulse.api:app --host 127.0.0.1 --port 8011
```

## Run tests

```bash
py -m pytest -q
# or
pytest -q
```

## CLI usage

### Multi-command (recommended)

```bash
trendpulse generate --theme "ai tools" --platform "tiktok" --region "global" --budget-mode balanced --task-type creative
```

### Legacy-compatible mode

```bash
trendpulse --theme "ai tools" --platform "tiktok" --region "global" --budget-mode balanced --task-type creative
```

## API examples

### Health

```bash
curl http://127.0.0.1:8011/health
```

### Ready

```bash
curl http://127.0.0.1:8011/ready
```

### Metrics

```bash
curl http://127.0.0.1:8011/metrics
```

### Generate

For Windows PowerShell (recommended to avoid escaping issues):

```powershell
$body = @{
  theme = "ai tools"
  platform = "tiktok"
  region = "global"
  budget_mode = "balanced"
  task_type = "creative"
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8011/v1/generate" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

## Docker

Build image:

```bash
docker build -t trendpulse:latest .
```

Run container:

```bash
docker run --rm -p 8011:8011 trendpulse:latest
```

## Docker Compose

```bash
docker compose up --build
```

Service runs at:

- `http://127.0.0.1:8011`

## Smoke scripts

- PowerShell: `scripts/smoke/smoke.ps1`
- Bash: `scripts/smoke/smoke.sh`

Examples:

```powershell
./scripts/smoke/smoke.ps1 -BaseUrl http://127.0.0.1:8011
```

```bash
bash scripts/smoke/smoke.sh http://127.0.0.1:8011
