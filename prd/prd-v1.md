# TrendPulse PRD v1

## 1. Product Summary

TrendPulse — AI-driven platform для выявления рыночных трендов и генерации игровых концептов/артефактов для студий.

## 2. Goals (MVP)

1. Сократить time-to-concept для игровых идей.
2. Повысить вероятность product-market fit через data-driven trend signals.
3. Дать воспроизводимый pipeline: signal -> analysis -> concept -> GDD draft.

## 3. Non-Goals (MVP)

1. Полноценный enterprise billing.
2. Полный набор всех data connectors.
3. Полноценный production-grade video generation pipeline.

## 4. Target Users

- Инди-студии
- Product managers в game teams
- Innovation/strategy команды у паблишеров

## 5. Core User Stories (MVP)

1. Как PM студии, я хочу получить список устойчивых трендов по тематике, чтобы выбирать направление прототипа.
2. Как геймдизайнер, я хочу сгенерировать pitch + базовый GDD, чтобы ускорить pre-production.
3. Как аналитик, я хочу видеть объяснение источников тренда, чтобы валидировать гипотезу.

## 6. Functional Scope (MVP)

1. LLM Gateway:
   - unified interface: chat/embed/stream_chat
   - providers: OpenRouter + Gemini
2. Ingestion MVP:
   - минимум 2 источника (social + finance)
3. Vector Brain:
   - embeddings storage + semantic retrieval
4. Idea Forge CLI/API:
   - генерация структурированного JSON результата

## 7. Non-Functional Requirements

- Надёжность: retry/circuit-breaker на вызовах провайдеров.
- Наблюдаемость: базовые метрики latency/errors/cost.
- Безопасность: API ключи только из env/secret manager.
- Масштабирование: асинхронный ingestion и очереди событий.

## 8. KPI (MVP)

1. Median time-to-first-concept <= 3 minutes.
2. Retrieval relevance baseline >= согласованного порога (offline eval).
3. Error rate по генерации < 5% на стандартном наборе сценариев.

## 9. Risks / Constraints

- ToS-ограничения источников данных и региональные ограничения.
- Высокая стоимость inference при сложном fallback.
- Drift качества контента и нестабильность внешних API.

## 10. Acceptance Criteria (MVP Exit)

1. Демо-сценарий от запроса до JSON-идеи проходит стабильно.
2. Есть базовые тесты контрактов LLM Gateway.
3. Есть логирование и trace-id для критичных этапов.
4. Документация по ограничениям и legal boundaries зафиксирована.
