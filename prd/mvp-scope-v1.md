# TrendPulse MVP Scope v1

## In Scope (MVP)

1. LLM Gateway с 2 провайдерами:
   - OpenRouter
   - Gemini
2. Базовый ingestion:
   - минимум 2 источника трендов
3. Retrieval baseline:
   - embeddings + semantic top-k retrieval
4. Idea generation:
   - CLI/API генерация структурированного JSON-концепта
5. Observability baseline:
   - trace_id, latency, provider/model logging

## Out of Scope (MVP)

1. Полный enterprise billing/quotas.
2. Полный набор коннекторов из всех индустрий.
3. Production-grade видео-генерация.
4. Полноценные Jira/Linear двусторонние интеграции.

## MVP Exit Criteria

1. Рабочий сквозной сценарий generate (>= 1 стандартный кейс стабильно).
2. Контрактные тесты LLM-интерфейса и retrieval schema.
3. Документированные ограничения/риски и roadmap следующей фазы.
