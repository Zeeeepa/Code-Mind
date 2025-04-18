"""Settings configuration for Code-Mind."""

import os
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()


class Settings(BaseModel):
    """Application settings."""

    # API settings
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    
    # UI settings
    ui_host: str = Field(default="0.0.0.0", description="UI host")
    ui_port: int = Field(default=8501, description="UI port")
    
    # LLM settings
    openai_api_key: Optional[str] = Field(
        default=None, description="OpenAI API key"
    )
    model_name: str = Field(
        default="gpt-4", description="Default model to use for code generation"
    )
    
    # Application settings
    debug: bool = Field(default=False, description="Debug mode")
    log_level: str = Field(default="INFO", description="Logging level")
    
    # Database settings
    database_url: Optional[str] = Field(
        default=None, description="Database connection URL"
    )
    
    class Config:
        """Pydantic config."""
        
        env_file = ".env"
        env_prefix = "CODE_MIND_"


@lru_cache()
def get_settings() -> Settings:
    """Get application settings.
    
    Returns:
        Settings: Application settings.
    """
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        database_url=os.getenv("DATABASE_URL"),
        debug=os.getenv("DEBUG", "False").lower() in ("true", "1", "t"),
    )
