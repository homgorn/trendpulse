# TrendPulse Epics v1

Источник: `prd/prd-v1.md`, `docs/bmad-project-audit-ru.md`

## Epic 1 — Platform Skeleton & Environments
**Outcome:** Базовый каркас проекта, конфиги окружений, безопасное хранение секретов.

### Candidate Stories
- Репозиторная структура `src/tests/docs/contracts`.
- Конфиг env + пример `.env.example`.
- Базовый logging/tracing bootstrap.

---

## Epic 2 — LLM Gateway MVP
**Outcome:** Единый интерфейс LLM и два провайдера (OpenRouter/Gemini).

### Candidate Stories
- Контракт `LLMBackend` (chat, stream_chat, embed).
- Реализация OpenRouter backend adapter.
- Реализация Gemini backend adapter.
- Router policy (primary/fallback).

---

## Epic 3 — Ingestion MVP
**Outcome:** Сбор трендовых сигналов из минимум 2 источников.

### Candidate Stories
- Connector social source (MVP).
- Connector finance source (MVP).
- Нормализация в единый event schema.

---

## Epic 4 — Vector Brain & Retrieval
**Outcome:** Семантический поиск по трендам.

### Candidate Stories
- Интеграция vector store.
- Индексация embeddings.
- Retrieval API с quality fields.

---

## Epic 5 — Idea Forge CLI/API
**Outcome:** Генерация структурированного JSON-питча.

### Candidate Stories
- CLI команда `trendpulse generate`.
- API endpoint для генерации.
- Формат результата: hypothesis/audience/monetization/risks.

---

## Epic 6 — Quality, Observability, Hardening
**Outcome:** Управляемая эксплуатация MVP.

### Candidate Stories
- Метрики latency/error/cost.
- Retry/circuit-breaker.
- Базовые contract/integration tests.
