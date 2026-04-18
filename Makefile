.PHONY: help install test lint format clean run run-docker build docker-build docker-up docker-down

help:
	@echo "TrendPulse Development Commands"
	@echo "================================"
	@echo "make install      - Install dependencies with uv"
	@echo "make test         - Run tests"
	@echo "make lint         - Run ruff linter"
	@echo "make format       - Format code with ruff"
	@echo "make clean        - Clean cache files"
	@echo "make run          - Run API locally"
	@echo "make run-docker   - Run with Docker"
	@echo "make docker-build - Build Docker image"
	@echo "make docker-up    - Start Docker Compose"
	@echo "make docker-down  - Stop Docker Compose"

install:
	uv sync

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check src/ api.py

format:
	uv run ruff format src/ api.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true

run:
	uv run uvicorn api:app --host 127.0.0.1 --port 8100 --reload

run-docker:
	docker run --rm -p 8100:8100 -v .env:/app/.env trendpulse:latest

docker-build:
	docker build -t trendpulse:latest .

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down
