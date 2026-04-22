from pydantic import field_validator
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://skillarena:skillarena_pass@localhost:5432/skillarena"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "your-super-secret-key-change-in-production-32chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    FRONTEND_URL: str = "http://localhost:5173"
    LICHESS_API_TOKEN: str = ""
    MAX_UPLOAD_SIZE_MB: int = 10

    @field_validator("DATABASE_URL")
    @classmethod
    def fix_postgres_url(cls, v: str) -> str:
        if v and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+asyncpg://", 1)
        if v and v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()
