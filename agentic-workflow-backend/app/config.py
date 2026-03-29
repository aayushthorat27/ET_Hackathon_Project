from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    log_level: str = "INFO"
    environment: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
