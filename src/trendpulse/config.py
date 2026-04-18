from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "trendpulse"
    app_env: str = "dev"
    log_level: str = "INFO"

    openrouter_api_key: str | None = None
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    gemini_api_key: str | None = None
    gemini_base_url: str = "https://generativelanguage.googleapis.com"

    default_provider: str = "openrouter"
    fallback_provider: str = "gemini"
    default_model: str = "openrouter/auto"

    llm_request_timeout_seconds: float = 30.0
    llm_max_retries: int = 1
    llm_retry_backoff_seconds: float = 0.25

    llm_circuit_breaker_fail_threshold: int = 3
    llm_circuit_breaker_open_seconds: float = 20.0

    cors_allowed_origins: str = "http://localhost:3000"
    rate_limit_requests: int = 30
    rate_limit_window_seconds: int = 60

    otel_enabled: bool = False
    otel_endpoint: str = "http://localhost:4317"

    database_url: str | None = None
    database_pool_size: int = 5
    database_max_overflow: int = 10

    valkey_url: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
