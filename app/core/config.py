"""Application configuration using pydantic-settings."""
from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Groq LLM configuration
    groq_api_key: str = Field(default="")
    groq_model: str = Field(default="openai/gpt-oss-120b")
    groq_temperature: float = Field(default=0.7)
    groq_max_tokens: int = Field(default=4000)
    groq_reasoning_effort: str = Field(default="low")

    # App settings
    app_name: str = Field(default="History Predictor")
    app_version: str = Field(default="0.1.0")
    debug: bool = Field(default=True)


settings = Settings()
