"""Configuration settings for Code-Mind."""
from functools import lru_cache
from typing import Optional
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """Application settings."""
    
    # API settings
    api_url: str = Field(
        "http://localhost:8000", 
        description="URL for the Code-Mind API"
    )
    
    # LLM settings
    openai_api_key: Optional[str] = Field(
        None, 
        description="OpenAI API key for LLM services"
    )
    model_name: str = Field(
        "gpt-4", 
        description="Default LLM model to use"
    )
    
    # Application settings
    debug: bool = Field(
        False, 
        description="Enable debug mode"
    )
    log_level: str = Field(
        "INFO", 
        description="Logging level"
    )
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_prefix = "CODE_MIND_"

@lru_cache()
def get_settings() -> Settings:
    """Get application settings, cached for performance."""
    return Settings()
