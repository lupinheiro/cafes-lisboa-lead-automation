from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/cafes_lisboa"
    )
    google_places_api_key: str = ""
    anthropic_api_key: str = ""
    resend_api_key: str = ""
    email_from: str = "prospecao@cafeslisboa.example"
    prospecting_region: str = "Minho, Portugal"
    frontend_origin: str = "http://localhost:5173"


@lru_cache
def get_settings() -> Settings:
    return Settings()
