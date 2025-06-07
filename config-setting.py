"""
Centralized configuration management using pydantic-settings.
All environment variables and settings in one place.
"""

from typing import Optional, Dict, Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, validator
from functools import lru_cache


class APISettings(BaseSettings):
    """API keys and endpoints configuration."""
    
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    google_api_key: Optional[str] = Field(None, env="GOOGLE_API_KEY")
    brave_api_key: Optional[str] = Field(None, env="BRAVE_API_KEY")
    github_token: Optional[str] = Field(None, env="GITHUB_TOKEN")
    deepseek_api_key: Optional[str] = Field(None, env="DEEPSEEK_API_KEY")
    
    # API endpoints
    deepseek_base_url: str = Field("https://api.deepseek.com/v1", env="DEEPSEEK_BASE_URL")
    
    @validator("openai_api_key", "brave_api_key", pre=True)
    def validate_required_keys(cls, v, field):
        if field.name in ["openai_api_key", "brave_api_key"] and not v:
            print(f"⚠️  Warning: {field.name.upper()} not set. Some features may be limited.")
        return v


class DatabaseSettings(BaseSettings):
    """Database configuration."""
    
    db_path: str = Field("data/memories.db", env="DB_PATH")
    db_backup_enabled: bool = Field(True, env="DB_BACKUP_ENABLED")
    db_backup_interval_hours: int = Field(24, env="DB_BACKUP_INTERVAL_HOURS")


class MemorySettings(BaseSettings):
    """Memory system configuration."""
    
    embedding_model: str = Field("text-embedding-3-small", env="EMBEDDING_MODEL")
    memory_compression_days: int = Field(30, env="MEMORY_COMPRESSION_DAYS")
    memory_archive_days: int = Field(90, env="MEMORY_ARCHIVE_DAYS")
    memory_search_limit: int = Field(100, env="MEMORY_SEARCH_LIMIT")
    similarity_threshold: float = Field(0.7, env="SIMILARITY_THRESHOLD")
    
    # Memory lifecycle settings
    min_memory_length: int = Field(100, env="MIN_MEMORY_LENGTH")
    memory_access_threshold: int = Field(5, env="MEMORY_ACCESS_THRESHOLD")


class RateLimitSettings(BaseSettings):
    """Rate limiting configuration."""
    
    # OpenAI
    openai_rpm: int = Field(500, env="OPENAI_REQUESTS_PER_MINUTE")
    openai_rph: int = Field(10000, env="OPENAI_REQUESTS_PER_HOUR")
    openai_burst: int = Field(20, env="OPENAI_BURST_SIZE")
    
    # Brave
    brave_rpm: int = Field(60, env="BRAVE_REQUESTS_PER_MINUTE")
    brave_burst: int = Field(5, env="BRAVE_BURST_SIZE")
    
    # GitHub
    github_rpm: int = Field(30, env="GITHUB_REQUESTS_PER_MINUTE")
    github_rph: int = Field(5000, env="GITHUB_REQUESTS_PER_HOUR")
    github_burst: int = Field(10, env="GITHUB_BURST_SIZE")


class AppSettings(BaseSettings):
    """General application settings."""
    
    app_name: str = Field("Docy Search", env="APP_NAME")
    app_version: str = Field("2.0.0", env="APP_VERSION")
    debug_mode: bool = Field(False, env="DEBUG")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    
    # UI settings
    streamlit_port: int = Field(8555, env="STREAMLIT_PORT")
    streamlit_theme: str = Field("dark", env="STREAMLIT_THEME")
    auto_refresh_interval: int = Field(5, env="AUTO_REFRESH_INTERVAL")
    
    # Model defaults
    default_ai_model: str = Field("openai", env="AI_MODEL")
    max_context_length: int = Field(8000, env="MAX_CONTEXT_LENGTH")
    
    # Feature flags
    enable_memory: bool = Field(True, env="ENABLE_MEMORY")
    enable_cost_tracking: bool = Field(True, env="ENABLE_COST_TRACKING")
    enable_activity_tracking: bool = Field(True, env="ENABLE_ACTIVITY_TRACKING")


class Settings(BaseSettings):
    """Main settings class combining all configurations."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Sub-configurations
    api: APISettings = Field(default_factory=APISettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    memory: MemorySettings = Field(default_factory=MemorySettings)
    rate_limits: RateLimitSettings = Field(default_factory=RateLimitSettings)
    app: AppSettings = Field(default_factory=AppSettings)
    
    def get_rate_limit_config(self, service: str) -> Dict[str, Any]:
        """Get rate limit configuration for a service."""
        configs = {
            "openai": {
                "requests_per_minute": self.rate_limits.openai_rpm,
                "requests_per_hour": self.rate_limits.openai_rph,
                "burst_size": self.rate_limits.openai_burst
            },
            "brave": {
                "requests_per_minute": self.rate_limits.brave_rpm,
                "burst_size": self.rate_limits.brave_burst
            },
            "github": {
                "requests_per_minute": self.rate_limits.github_rpm,
                "requests_per_hour": self.rate_limits.github_rph,
                "burst_size": self.rate_limits.github_burst
            }
        }
        return configs.get(service, {"requests_per_minute": 60})
    
    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        """Get configuration for a specific AI model."""
        configs = {
            "openai": {
                "api_key": self.api.openai_api_key,
                "model": "gpt-4o-mini"
            },
            "claude": {
                "api_key": self.api.anthropic_api_key,
                "model": "claude-3-opus-20240229"
            },
            "gemini": {
                "api_key": self.api.google_api_key,
                "model": "gemini-1.5-flash"
            },
            "deepseek": {
                "api_key": self.api.deepseek_api_key,
                "model": "deepseek-chat",
                "base_url": self.api.deepseek_base_url
            }
        }
        return configs.get(model_name, configs["openai"])
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.app.debug_mode


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Usage examples:
"""
# In any file:
from config.settings import get_settings

settings = get_settings()

# Access API keys
openai_key = settings.api.openai_api_key

# Get rate limit config
rate_config = settings.get_rate_limit_config("openai")

# Check feature flags
if settings.app.enable_memory:
    # Use memory system

# Get model configuration
model_config = settings.get_model_config("claude")
"""