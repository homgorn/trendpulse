# Event Schema v1 (TrendPulse)

## Цель

Унифицировать события между ingestion, processing, retrieval и orchestration.

## Envelope (обязательный для всех событий)

```json
{
  "event_id": "uuid",
  "event_type": "trend.ingested.v1",
  "event_version": "v1",
  "occurred_at": "2026-03-05T10:00:00Z",
  "trace_id": "uuid",
  "source": "connector:tiktok",
  "tenant_id": "default",
  "payload": {}
}
```

## Event Types (v1)

1. `trend.ingested.v1`
2. `trend.normalized.v1`
3. `embedding.created.v1`
4. `retrieval.completed.v1`
5. `idea.generated.v1`
6. `pipeline.failed.v1`

---

## 1) trend.ingested.v1

```json
{
  "source_platform": "tiktok",
  "source_region": "global",
  "raw_item_id": "abc123",
  "raw_text": "string",
  "raw_tags": ["tag1", "tag2"],
  "collected_at": "2026-03-05T10:00:00Z"
}
```

Validation:
- `source_platform` required
- хотя бы одно из `raw_text` или `raw_tags` должно быть непустым

---

## 2) trend.normalized.v1

```json
{
  "canonical_id": "trend_001",
  "language": "en",
  "normalized_text": "string",
  "entities": ["entity1"],
  "signals": {
    "velocity": 0.72,
    "volatility": 0.34
  }
}
```

Validation:
- `canonical_id` required
- `signals.velocity` в диапазоне [0,1]

---

## 3) embedding.created.v1

```json
{
  "canonical_id": "trend_001",
  "embedding_model": "text-embedding-3-large",
  "vector_dim": 3072,
  "store": "qdrant",
  "status": "ok"
}
```

Validation:
- `vector_dim` > 0
- `status` in `ok|failed`

---

## 4) retrieval.completed.v1

```json
{
  "query": "mobile crypto cats",
  "top_k": 10,
  "results_count": 10,
  "latency_ms": 143,
  "quality": {
    "semantic_score_avg": 0.81
  }
}
```

Validation:
- `top_k` > 0
- `results_count` >= 0

---

## 5) idea.generated.v1

```json
{
  "idea_id": "idea_001",
  "theme": "crypto",
  "platform": "mobile",
  "provider_used": "openrouter",
  "model_used": "qwen/qwen-2.5-72b-instruct",
  "output_schema_version": "v1"
}
```

Validation:
- `idea_id` required
- `output_schema_version` required

---

## 6) pipeline.failed.v1

```json
{
  "stage": "retrieval",
  "error_code": "PROVIDER_TIMEOUT",
  "error_message": "timeout waiting provider",
  "retryable": true
}
```

Validation:
- `stage` required
- `error_code` required

---

## Compatibility Rules

1. Backward-compatible changes: добавление optional полей.
2. Breaking changes: только через новую версию event (`*.v2`) + migration note.
3. Все события обязаны нести `trace_id` для сквозной диагностики.
