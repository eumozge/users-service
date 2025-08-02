from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="POSTGRES_",
        extra="ignore",
    )
    host: str = "localhost"
    port: int = 5432
    db: str = "postgres"
    user: str = "postgres"
    password: str = "password"

    @property
    def asyncurl(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    @property
    def syncurl(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class APISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="API_",
        extra="ignore",
    )
    host: str = "localhost"
    port: int = 8000
    debug: bool = __debug__


class LogSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="LOG_",
        extra="ignore",
    )
    path: Path = Path("users.log")
    level: str = "DEBUG"


class Settings(BaseSettings):
    db: DBSettings = Field(
        default_factory=lambda: DBSettings(),
    )
    api: APISettings = Field(
        default_factory=lambda: APISettings(),
    )
    logs: LogSettings = Field(
        default_factory=lambda: LogSettings(),
    )


settings = Settings()
