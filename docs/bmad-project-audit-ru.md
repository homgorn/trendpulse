# TrendPulse — BMAD аудит и декомпозиция (RU)

## 1) Что это за проект (по текущим спецификациям)

TrendPulse Engine — AI-платформа для market intelligence в game dev:
- собирает и нормализует тренды из нескольких индустрий;
- строит семантический поиск (RAG + vector DB);
- генерирует игровые концепты, GDD, визуальные ассеты;
- даёт API/интеграции для студий (Jira/Linear/Webhooks);
- использует модульный LLM Gateway с провайдерами и fallback-логикой.

Ключевая архитектурная идея: **microkernel + plugin modules + event-driven orchestration**.

---

## 2) Консолидация двух spec-файлов

В проекте есть два документа:
- `spec.txt` — подробно описывает LLM-слой и roadmap интеграции провайдеров.
- `first spec.txt` — задаёт продуктовую картину, модульную архитектуру и roadmap по фазам продукта.

Они **не конфликтуют**, а дополняют друг друга:
- `first spec.txt`: "зачем и что делаем" (продукт, value, use-cases, high-level arch).
- `spec.txt`: "как делаем LLM-часть" (интерфейс, провайдеры, спринты, SDK).

---

## 3) BMAD-декомпозиция

## 3.1 Vision / Product intent
- Цель: сократить риск “строим игру не для реального спроса”.
- Outcome: pipeline от сырого шума/сигналов рынка до готовых продуктовых артефактов (idea pitch, GDD, asset prompts).
- ICP (первично): инди и mid-size game studios, innovation teams, publisher scouting teams.

## 3.2 PRD scope (MVP -> Growth)
### MVP Scope (Phase 1)
1. LLM Gateway (OpenRouter + Gemini минимум).
2. Ingestion connectors: TikTok trends + crypto source.
3. Vector Brain: Qdrant + metadata store.
4. CLI генерация идеи: `trendpulse generate ...`.
5. JSON output с объяснимыми полями (hypothesis, audience, monetization).

### Phase 2
1. Agentic orchestration (LangGraph роли).
2. Web UI (Next.js dashboard).
3. Basic image generation pipeline.
4. Additional sources/connectors.

### Phase 3
1. Enterprise API + webhooks.
2. MCP server.
3. Rate limits/billing.
4. Расширение модельного пула (в т.ч. Chinese providers).

## 3.3 Architecture (target state)
Слои:
1. **Ingestion Core** — асинхронный сбор, нормализация, event bus.
2. **Vector Brain** — embeddings + retrieval.
3. **LLM Gateway** — единый интерфейс + адаптеры провайдеров.
4. **Agentic Orchestrator** — маршрутизация задач между ролями.
5. **Generative Media** — генерация изображений/превью.
6. **Interfaces** — API + Web + CLI + MCP.

Принцип: ядро не знает о конкретном провайдере, только о `LLMBackend`.

## 3.4 Epics (backlog starter)
1. Epic A — Core Platform Skeleton
2. Epic B — LLM Gateway + Provider Adapters
3. Epic C — Data Ingestion + Trend Normalization
4. Epic D — Vector Brain + RAG
5. Epic E — Idea Forge CLI/API
6. Epic F — Agentic Orchestration
7. Epic G — Web UI + Project Workspace
8. Epic H — Enterprise Integrations (Jira/Linear/Webhooks)
9. Epic I — MCP Exposure
10. Epic J — Reliability, Observability, Security

## 3.5 Risks / Constraints (production-minded)
- API ToS/региональные ограничения источников данных.
- Стоимость inference при multi-provider fallback.
- Качество и drift сигналов (хайп vs устойчивый тренд).
- Правовые режимы по регионам (контент, персональные данные, age-gating).
- Vendor lock-in (минимизируется через unified gateway).

## 3.6 Compliance baseline (для “легально где разрешено”)
- Гео-фильтрация и feature flags по юрисдикциям.
- Source allowlist + terms-aware ingestion.
- Data minimization + no raw PII ingestion.
- Age/Content policy gates.
- Audit logs по данным, промптам и решениям агентов.

---

## 4) Production roadmap (BMAD-friendly)

## Sprint 0 — Foundation
- Repo conventions, env strategy, secrets handling.
- Определить контракты модулей (interfaces first).
- Поднять базовые окружения (dev/stage).

## Sprint 1 — Core + LLM Gateway MVP
- `LLMBackend` interface + OpenRouter/Gemini adapters.
- Model registry + fallback routing policy.
- Contract tests на chat/embed/stream.

## Sprint 2 — Ingestion MVP + Vector Brain
- Первые коннекторы (TikTok/crypto).
- Normalization pipeline + embeddings ingestion.
- Qdrant retrieval с baseline relevance metrics.

## Sprint 3 — Idea Forge CLI/API
- Генерация структурированного pitch JSON.
- Quality scoring (novelty/feasibility/market fit).
- Baseline prompt packs versioning.

## Sprint 4 — Agentic orchestration
- LangGraph multi-agent pipeline.
- Critic loop + self-check gates.
- Memory strategy (short/long term).

## Sprint 5 — Web app MVP
- Dashboard, query flow, saved concepts.
- Basic SEO pages for generated ideas.
- RBAC lite + user workspace.

## Sprint 6 — Enterprise + MCP
- Webhooks + Jira/Linear integration.
- MCP tools exposure.
- Rate limits, usage metering, billing hooks.

## Sprint 7 — Hardening
- Observability, SLO, error budgets.
- Security review + abuse controls.
- Load/perf tests and cost optimization.

---

## 5) Что проверять в интернете (официальные источники)

Проверять только:
- актуальность SDK/версий;
- API compatibility statements (OpenAI-compatible);
- лимиты/квоты и auth flow;
- текущие названия моделей и deprecated endpoints.

Критично перепроверять перед кодом:
- OpenRouter, Google Gemini, OpenAI, Anthropic, MCP, Together, Fireworks, Groq, Qwen, GLM, DeepSeek, LangGraph.

---

## 6) Как использовать BMAD в этом проекте (практика)

1. Вести артефакты проекта в `trendpulse/` (не трогая `_bmad` ядро).
2. Формализовать:
   - PRD,
   - Architecture,
   - Epics/Stories,
   - Sprint plan.
3. Генерировать/обновлять артефакты через BMAD workflow-подход.
4. Хранить все project docs рядом с кодом проекта для трассируемости решений.

Рекомендуемая структура внутри `trendpulse`:
- `docs/` — архитектура, ADR, roadmap, compliance.
- `prd/` — PRD и scope.
- `backlog/` — epics/stories/sprint plans.
- `contracts/` — интерфейсы модулей и API схемы.
- `src/` — реализация.
- `tests/` — contract/integration/e2e.

---

## 7) Итог

Проект описан достаточно сильно для старта production-подхода:
- есть ясная vision/value;
- есть модульная архитектура;
- есть реалистичный roadmap;
- есть стратегия по multi-provider LLM.

Следующий практический шаг: зафиксировать **интерфейсные контракты** (LLM, ingestion events, retrieval schema) и от них строить реализацию.
