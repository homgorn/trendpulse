---
title: TrendPulse — ИИ-платформа для игровой индустрии
description: TrendPulse — открытая ИИ-платформа для игровых студий. Мониторинг трендов и генерация игровых концепций. Мульти-провайдер LLM роутинг, RAG, circuit breaker.
keywords: разработка игр, маркетинговый анализ, ИИ для игр, анализ трендов, дизайн игр, LLM, генератор GDD, тренды игровой индустрии
author: TrendPulse Team
robots: index, follow
og:title: TrendPulse — ИИ для игровой индустрии
og:description: Превращаем рыночный шум в успешные игры с помощью ИИ
og:type: website
og:url: https://homgorn.github.io/trendpulse/
og:locale: ru_RU
og:image: https://homgorn.github.io/trendpulse/og-image.png
twitter:card: summary_large_image
twitter:title: TrendPulse — ИИ для игровой индустрии
twitter:description: Превращаем рыночный шум в успешные игры
---

# TrendPulse — ИИ Маркетинговый Анализ для Геймдева

<p align="center">
  <a href="https://pypi.org/project/trendpulse/"><img src="https://img.shields.io/badge/version-0.2.0-blue.svg" alt="Version"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.11%2B-green.svg" alt="Python"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License"></a>
  <a href="https://github.com/homgorn/trendpulse/actions"><img src="https://img.shields.io/badge/status-Gotov-brightgreen.svg" alt="Status"></a>
</p>

**TrendPulse** — открытая ИИ-платформа для игровых студий. Мониторинг трендов и генерация игровых концепций. Мульти-провайдер LLM (OpenRouter, Gemini), RAG, circuit breaker, rate limiting.

| [English](README.md) | [Русский](README-RU.md) | [Docs](docs/) | [Инвесторам](investors/) | [GitHub](https://github.com/homgorn/trendpulse) |

## Быстрый Старт

```bash
pip install trendpulse
export OPENROUTER_API_KEY=ваш_ключ
trendpulse generate --theme "королевская битва" --platform mobile
```

Или через Docker:

```bash
docker run -p 8000:8000 -e OPENROUTER_API_KEY=ваш_ключ ghcr.io/homgorn/trendpulse:latest
```

---

## Возможности

| Возможность | Описание |
|------------|---------|
| **REST API** | FastAPI с эндпоинтами `/health`, `/ready`, `/metrics`, `/v1/generate` |
| **CLI** | Командная строка для генерации |
| **Мульти-LLM** | OpenRouter (300+ моделей) + Google Gemini с авто-fallback |
| **Circuit Breaker** | Настраиваемый порог ошибок и таймаут восстановления |
| **Rate Limiting** | Встроенный лимитер запросов |
| **Мониторинг** | Prometheus метрики, OpenTelemetry |
| **Обработка Ошибок** | Структурированные коды ошибок с HTTP статусами |

---

## Архитектура

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   REST API   │--->│   Service  │--->│  LLM Gateway│
│   (FastAPI) │    │ (Business │    │(Routing + │
└──────────────┘    │   Logic)  │    │ Fallback) │
                   └──────────────┘    └────┬───────┘
                                           │
         ┌──────────────────────────────┼───────────────┐
         │     Adapters Layer         │            │
         │ ┌────────────┐  ┌────────┐  │            │
         │ │OpenRouter│  │ Gemini │  │            │
         │ └────────────┘  └────────┘  │            │
         └──────────────────────────────────────────┘
```

**Ядро**: API (`api.py`), Service (`service.py`), Gateway (`gateway.py`), Adapters (OpenRouter, Gemini)

---

## Установка

### Требования

- Python 3.11+
- API ключ хотя бы одного LLM провайдера

### Установка пакета

```bash
pip install trendpulse
```

### Из исходников

```bash
git clone https://github.com/homgorn/trendpulse.git
cd trendpulse
pip install -e ".[dev]"
```

### Настройка .env

```env
OPENROUTER_API_KEY=sk-or-...
GEMINI_API_KEY=...

DEFAULT_PROVIDER=openrouter
FALLBACK_PROVIDER=gemini
LOG_LEVEL=INFO

RATE_LIMIT_REQUESTS=30
RATE_LIMIT_WINDOW_SECONDS=60
```

### Запуск

```bash
uvicorn trendpulse.api:app --host 127.0.0.1 --port 8100 --reload
```

API: `http://127.0.0.1:8100`

---

## API Эндпоинты

### GET /health

Всегда возвращает `{"status": "ok"}`

```bash
curl http://127.0.0.1:8100/health
```

### GET /ready

Проверка готовности LLM провайдера

```bash
curl http://127.0.0.1:8100/ready
```

### GET /metrics

Prometheus метрики

```bash
curl http://127.0.0.1:8100/metrics
```

### POST /v1/generate

Генерация игровой концепции

**Запрос:**

```json
{
  "theme": "искусственный интеллект",
  "platform": "tiktok",
  "region": "global",
  "budget_mode": "balanced",
  "task_type": "creative"
}
```

**Ответ:**

```json
{
  "idea": "ИИ-видео редактор...",
  "audience": "Gen Z контент креаторы...",
  "monetization": "Фримиум с премиум...",
  "risks": ["Насыщенность рынка", "Зависимость от платформы"],
  "sources": ["TikTok тренды", "Product Hunt"],
  "provider": "openrouter"
}
```

---

## CLI

```bash
trendpulse generate \
  --theme "искусственный интеллект" \
  --platform "tiktok" \
  --region "global" \
  --budget-mode balanced \
  --task-type creative
```

---

## Конфигурация

| Переменная | По умолчанию | Описание |
|----------|--------------|---------|
| `OPENROUTER_API_KEY` | — | OpenRouter ключ |
| `GEMINI_API_KEY` | — | Google Gemini ключ |
| `DEFAULT_PROVIDER` | openrouter | Основной провайдер |
| `FALLBACK_PROVIDER` | gemini | Резервный провайдер |
| `LLM_REQUEST_TIMEOUT_SECONDS` | 30 | Таймаут запроса |
| `RATE_LIMIT_REQUESTS` | 30 | Запросов в окно |
| `RATE_LIMIT_WINDOW_SECONDS` | 60 | Окно в секундах |

---

## Docker

```bash
docker build -t trendpulse:latest .
docker run --rm -p 8100:8100 -v .env:/app/.env trendpulse:latest
```

---

## Тесты

```bash
pytest -v
ruff check src/
```

---

## Контрибуция

1. Форк репозитория
2. Ветка для фичи
3. Изменения + тесты
4. Пулл-реквест

---

## Лицензия

MIT — см. [LICENSE](LICENSE)

---

<p align="center">Сделано с ❤️ для игровых студий</p>