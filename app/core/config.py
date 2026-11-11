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
    groq_model: str = Field(default="llama-3.3-70b-versatile")
    groq_temperature: float = Field(default=0.7)
    groq_max_tokens: int = Field(default=4096)

    # App settings
    app_name: str = Field(default="History Predictor")
    app_version: str = Field(default="0.1.0")
    debug: bool = Field(default=True)

    # Database
    database_url: str = Field(default="sqlite:///./history_predictor.db")

    # Vector DB (Phase 2)
    chroma_host: str = Field(default="localhost")
    chroma_port: int = Field(default=8000)

    # Cache
    redis_url: str = Field(default="redis://localhost:6379/0")


settings = Settings()
