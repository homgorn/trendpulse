# Retrieval Schema v1 (TrendPulse)

## Цель

Стандартизировать контракт запроса/ответа retrieval-слоя для RAG и аналитики трендов.

## Request Schema (v1)

```json
{
  "query": "mobile crypto cats",
  "filters": {
    "region": ["global", "cn"],
    "sources": ["tiktok", "coingecko"],
    "time_window_days": 14
  },
  "top_k": 10,
  "include_metadata": true,
  "include_vectors": false,
  "rerank": {
    "enabled": true,
    "strategy": "hybrid"
  }
}
```

### Request Validation
1. `query` required, min length = 2.
2. `top_k` required, range [1..100].
3. `time_window_days` optional, range [1..365].

---

## Response Schema (v1)

```json
{
  "request_id": "uuid",
  "trace_id": "uuid",
  "query": "mobile crypto cats",
  "results": [
    {
      "canonical_id": "trend_001",
      "score": 0.89,
      "rank": 1,
      "snippet": "Trend description",
      "entities": ["gacha", "memecoin"],
      "source_refs": [
        {
          "platform": "tiktok",
          "item_id": "abc123",
          "url": "https://example.com/item"
        }
      ],
      "metadata": {
        "language": "en",
        "region": "global",
        "updated_at": "2026-03-05T10:00:00Z"
      }
    }
  ],
  "quality": {
    "semantic_score_avg": 0.81,
    "diversity_score": 0.62,
    "freshness_score": 0.74
  },
  "latency_ms": 143
}
```

### Response Validation
1. `request_id` and `trace_id` required.
2. `results[*].score` range [0..1].
3. `results[*].rank` starts at 1 and unique inside response.
4. `latency_ms` >= 0.

---

## Error Schema (v1)

```json
{
  "request_id": "uuid",
  "trace_id": "uuid",
  "error": {
    "code": "RETRIEVAL_BACKEND_UNAVAILABLE",
    "message": "Qdrant unavailable",
    "retryable": true
  }
}
```

### Error Codes (minimum)
- `INVALID_REQUEST`
- `RETRIEVAL_BACKEND_UNAVAILABLE`
- `TIME_WINDOW_OUT_OF_RANGE`
- `TOP_K_OUT_OF_RANGE`
- `UNKNOWN`

---

## Versioning Rules

1. Optional fields can be added within v1.
2. Removing/renaming required fields = v2.
3. Клиенты должны игнорировать неизвестные optional поля.
