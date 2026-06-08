# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict # Pydantic extension for configuration

class Settings(BaseSettings):
    DATABASE_URL: str # no default
    SECRET_KEY: str # no default
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # expires after 30 mins

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()

# app shouldn't run w/o DB URL or signing key