from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "ACHARYA SAFE"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        extra="ignore"
    )


settings = Settings()