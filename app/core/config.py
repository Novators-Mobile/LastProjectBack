from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
        case_sensitive=False,
    )

    app_env: str = Field(default="dev", validation_alias="APP_ENV")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")

    database_url: str = Field(
        default="postgresql+psycopg2://postgres:postgres@db:5432/app",
        validation_alias="DATABASE_URL",
    )
    storage_dir: str = Field(default="storage", validation_alias="STORAGE_DIR")

    auth_disabled: bool = Field(default=True, validation_alias="AUTH_DISABLED")
    access_token: str = Field(default="changeme", validation_alias="ACCESS_TOKEN")


settings = Settings()
