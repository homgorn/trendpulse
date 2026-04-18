# TrendPulse — Stories Sprint 01

Связанные документы:
- `prd/prd-v1.md`
- `backlog/epics-v1.md`
- `contracts/llm-backend-interface-v1.md`

## Sprint Goal

Собрать “сквозной” MVP-поток:
LLM Gateway (OpenRouter + Gemini) -> базовый ingestion mock -> retrieval mock -> JSON-концепт через CLI.

---

## Story S1-01 — LLMBackend interface scaffold

**Как** backend-разработчик  
**Я хочу** реализовать интерфейсный каркас `LLMBackend`  
**Чтобы** все провайдеры подключались единообразно.

### Acceptance Criteria
1. Есть интерфейсный модуль с методами `chat`, `stream_chat`, `embed`.
2. Есть единый набор доменных ошибок.
3. Есть базовый контрактный тест на сигнатуры и валидацию входа.

---

## Story S1-02 — OpenRouter adapter (MVP)

**Как** платформа  
**Я хочу** иметь рабочий OpenRouter adapter  
**Чтобы** использовать его как default provider.

### Acceptance Criteria
1. Adapter поддерживает `chat` и `embed`.
2. Конфиг читается из env (`OPENROUTER_API_KEY`, optional base URL).
3. Ошибки API маппятся в доменные исключения.
4. Есть smoke-test с mock/fake transport.

---

## Story S1-03 — Gemini adapter (MVP)

**Как** платформа  
**Я хочу** Gemini adapter  
**Чтобы** иметь второй провайдер для fallback.

### Acceptance Criteria
1. Adapter поддерживает `chat` (embed как optional в sprint 1).
2. Конфиг читается из env (`GEMINI_API_KEY`).
3. Добавлена стратегия fallback OpenRouter <-> Gemini.
4. Есть тест на переключение провайдера при ошибке primary.

---

## Story S1-04 — Model routing policy v1

**Как** оркестратор  
**Я хочу** правило выбора модели/провайдера  
**Чтобы** уменьшить latency и cost.

### Acceptance Criteria
1. Есть policy-функция с входом: task_type, budget_mode, region.
2. Есть минимум 3 профиля: reasoning, creative, balanced.
3. Решение policy логируется с trace-id.

---

## Story S1-05 — CLI generate (JSON output)

**Как** product owner  
**Я хочу** CLI-команду генерации концепта  
**Чтобы** быстро тестировать value без UI.

### Acceptance Criteria
1. Команда формата `trendpulse generate --theme=... --platform=...`.
2. Вывод: валидный JSON (idea, audience, monetization, risks, sources).
3. В случае ошибки возвращается структурированный error JSON.

---

## Story S1-06 — Observability baseline

**Как** инженер эксплуатации  
**Я хочу** базовые метрики и трейсинг  
**Чтобы** видеть деградации на ранней стадии.

### Acceptance Criteria
1. Лог содержит `trace_id`, `provider`, `model`, `latency_ms`.
2. Счётчики ошибок по провайдерам.
3. Отчёт о token/cost при наличии данных у провайдера.

---

## Definition of Done (Sprint 01)

1. Все story acceptance criteria выполнены.
2. Contract tests и smoke tests проходят.
3. Документация обновлена (PRD/Contracts/Backlog согласованы).
4. Демо-команда CLI работает на тестовом сценарии.
