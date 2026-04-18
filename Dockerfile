# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./

# Install dependencies (frozen, no dev)
RUN uv sync --frozen --no-dev

# Stage 2: Runtime
FROM python:3.12-slim AS runtime

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv

# Copy application code
COPY src/ ./src/
COPY api.py ./

# Ensure venv is in PATH
ENV PATH="/app/.venv/bin:$PATH"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8100/status || exit 1

EXPOSE 8100

# Run with uvicorn (1 process for K8s, use HPA for scaling)
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8100"]
