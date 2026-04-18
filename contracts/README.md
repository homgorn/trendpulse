# TrendPulse Contracts Workspace

Контракты интерфейсов и схемы обмена между модулями.

## Содержимое

- `llm-backend-interface-v1.md` — единый контракт `LLMBackend` (chat/stream/embed).
- `event-schema-v1.md` — события ingestion/processing/orchestration.
- `retrieval-schema-v1.md` — схема retrieval-запросов/ответов и quality fields.
- `provider-capabilities-matrix-v1.md` — матрица возможностей провайдеров (chat, tool-use, vision, embeddings, streaming).

## Правила

1. Сначала контракт, потом реализация.
2. Любой breaking change фиксировать как новая версия (`v2` и т.д.).
3. Контракты должны быть независимы от конкретного провайдера.
