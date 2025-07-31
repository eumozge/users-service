from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
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
    password: str = Field(..., min_length=1)

    @property
    def asyncurl(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    @property
    def syncurl(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class Settings(BaseSettings):
    db: PostgresSettings = Field(
        default_factory=lambda: PostgresSettings(),
    )


settings = Settings()
