"""Application settings using Pydantic for validation."""

from typing import Optional  # Optional[T] = Union[T, None]
# Pydantic: Data validation using Python type annotations
# Why: Validates types, parses env vars, provides defaults, raises errors on invalid config
from pydantic_settings import BaseSettings
from functools import lru_cache  # Least Recently Used cache decorator


# BaseSettings: Pydantic class that auto-loads config from environment variables
# Why: Type-safe config, auto-parsing, validation, .env file support
# Pattern: Centralized configuration management (12-factor app)
class Settings(BaseSettings):
    """Application configuration with environment variable support."""
    
    # Azure Event Hub settings
    # Optional[str] = Union[str, None] - can be string or None (not required)
    event_hub_connection_string: Optional[str] = None  # Loaded from EVENT_HUB_CONNECTION_STRING
    event_hub_name: Optional[str] = None  # Loaded from EVENT_HUB_NAME
    
    # Azure AI Search settings
    search_endpoint: Optional[str] = None
    search_api_key: Optional[str] = None
    search_index_name: str = "fruits-quality"
    
    # Detection settings
    yolo_model: str = "yolov8n.pt"
    detection_confidence: float = 0.3
    
    # Video settings
    default_camera_source: str = "0"
    output_directory: str = "output"
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# @lru_cache: Caches function results (memoization)
# Why: Ensures get_settings() returns same instance every time (singleton pattern)
# Pattern: Prevents re-loading .env file on every call, saves memory
# Result: First call creates Settings, subsequent calls return cached instance
@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Uses LRU cache to ensure singleton pattern.
    """
    return Settings()  # Only executed once, then cached
