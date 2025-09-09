from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_", extra="ignore")

    app_name: str = "rl-dda-demo-back"

    # Database: mysql+aiomysql (pure-Python for Windows compatibility)
    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_user: str = "app"
    db_password: str = "app"
    db_name: str = "rldda"

    # Optional full DSN override
    database_url: Optional[str] = None

    # CORS
    cors_origins: List[str] = []

    # Ingest token
    ingest_secret: str = "change-me"

    # Storage (S3/MinIO)
    s3_endpoint_url: Optional[str] = None
    s3_region_name: Optional[str] = None
    s3_access_key_id: Optional[str] = None
    s3_secret_access_key: Optional[str] = None
    s3_bucket: Optional[str] = None

    @property
    def sqlalchemy_dsn(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"mysql+aiomysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


