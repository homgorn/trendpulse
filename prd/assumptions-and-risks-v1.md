# TrendPulse Assumptions and Risks v1

## Assumptions

1. Доступ к ключевым API источников сохраняется в целевых регионах.
2. Стоимость inference укладывается в целевую экономику MVP.
3. Качества retrieval достаточно для генерации полезных гипотез.
4. Команда готова поддерживать multi-provider конфигурацию.

## Key Risks

## R1 — Source/API policy changes
- Impact: высокий
- Mitigation: source allowlist, adapter isolation, fallback connectors

## R2 — Cost blow-up on LLM calls
- Impact: высокий
- Mitigation: routing policy, token budgets, caching, cheaper fallback models

## R3 — Low retrieval relevance
- Impact: высокий
- Mitigation: quality eval loop, rerank strategy, better normalization

## R4 — Provider instability / outages
- Impact: средний/высокий
- Mitigation: retry + circuit breaker + provider fallback chain

## R5 — Compliance variance by region
- Impact: высокий
- Mitigation: geo feature flags, legal gating, content policy checks

## Monitoring Signals

1. Error rate by provider/model
2. Cost per generated concept
3. Retrieval quality scores (offline/online proxies)
4. End-to-end latency (p50/p95)
