from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = (
        "postgresql+psycopg2://integration_hub:integration_hub@localhost:5432/integration_hub"
    )

    api_username: str = "admin"
    api_password: str = "admin"
    jwt_secret_key: str = "change-me-in-production-this-default-is-not-secure"
    jwt_algorithm: str = "HS256"
    jwt_expires_minutes: int = 30


@lru_cache
def get_settings() -> Settings:
    return Settings()
