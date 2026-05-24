from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore',
    )

    database_url: str = Field(
        default='postgresql+asyncpg://financas:financas@localhost:5432/financas'
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
