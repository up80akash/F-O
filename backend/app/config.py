from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "fo-trading-platform"
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "dev-secret"
    jwt_secret: str = "dev-jwt-secret"
    database_url: str = "postgresql://postgres:postgres@postgres:5432/trading_db"
    redis_url: str = "redis://redis:6379/0"
    trading_mode: str = "PAPER"
    live_trading_enabled: bool = False
    broker_api_enabled: bool = False
    broker_api_base_url: str = ""
    broker_api_token: str = ""
    broker_api_auth_header: str = "Authorization"
    broker_api_auth_scheme: str = "Bearer"
    broker_api_timeout_seconds: float = 10.0
    broker_api_quote_path: str = "/quote/{symbol}"
    broker_api_quotes_path: str = "/quotes"
    broker_api_option_chain_path: str = "/option-chain"
    broker_api_positions_path: str = "/positions"
    broker_api_orders_path: str = "/orders"
    broker_api_order_path: str = "/orders/{order_id}"
    broker_api_instruments_path: str = "/instruments"
    ollama_base_url: str = "http://ollama:11434"
    ai_model: str = "llama3.1"
    allowed_hosts: str = "localhost,127.0.0.1"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
