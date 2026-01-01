"""Configuration management using Pydantic BaseSettings."""
from typing import Optional

try:
    # Pydantic v2
    from pydantic_settings import BaseSettings
    from pydantic import Field
except ImportError:
    # Pydantic v1
    from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    supabase_url: str = Field(..., env="SUPABASE_URL", description="Supabase project URL")
    supabase_key: str = Field(..., env="SUPABASE_KEY", description="Supabase anon/service key")
    
    # Optional settings with defaults
    supabase_storage_bucket: str = Field(
        default="scans",
        env="SUPABASE_STORAGE_BUCKET",
        description="Supabase storage bucket name for scan images"
    )
    
    api_title: str = Field(
        default="RheumaLens API",
        env="API_TITLE",
        description="API title"
    )
    
    api_version: str = Field(
        default="1.0.0",
        env="API_VERSION",
        description="API version"
    )
    
    debug: bool = Field(
        default=False,
        env="DEBUG",
        description="Debug mode"
    )
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings: Settings = Settings()

