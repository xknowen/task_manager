from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR.parent / ".env"


class Settings(BaseSettings):
    app_name: str = "Task Manager API"
    database_url: str
    test_database_url: str | None = None
    debug: bool = False
    allowed_hosts: list[str] = ["localhost"]

    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
