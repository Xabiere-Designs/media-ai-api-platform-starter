from functools import cached_property

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    app_name: str = "Media AI Platform API"
    app_version: str = "2.0.0"
    environment: str = "local"
    debug: bool = False
    api_prefix: str = "/v1"

    database_url: str = Field(default="sqlite:///./mediaai.db", alias="DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    jwt_secret_key: str = Field(default="change-me", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    cache_ttl_seconds: int = Field(default=300, alias="CACHE_TTL_SECONDS")
    enable_metrics: bool = Field(default=True, alias="ENABLE_METRICS")
    enable_redis_cache: bool = Field(default=True, alias="ENABLE_REDIS_CACHE")
    allowed_origins: str = Field(default="http://localhost:3000,http://localhost:8000", alias="ALLOWED_ORIGINS")

    @cached_property
    def allowed_origins_list(self) -> list[str]:
        return [item.strip() for item in self.allowed_origins.split(",") if item.strip()]


settings = Settings()
