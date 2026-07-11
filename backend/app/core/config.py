from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


BASE_DIR = Path(
    __file__
).resolve().parents[2]


class Settings(BaseSettings):

    # Application

    app_name: str

    app_version: str

    app_description: str


    # Debug

    debug: bool


    # Server

    host: str

    port: int


    # Database

    database_url: str


    # JWT

    secret_key: str

    algorithm: str

    access_token_expire_minutes: int


    # AI provider

    ai_provider: str = "openai"

    openai_api_key: str | None = None

    ai_model: str = "gpt-4.1-mini"

    ai_temperature: float = 0.7

    ai_max_tokens: int = 1000

    ai_timeout_seconds: float = 30.0

    ai_max_history_messages: int = 20

    ai_max_memories: int = 10


    # Pydantic settings configuration

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()