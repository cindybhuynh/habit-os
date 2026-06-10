# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict # Pydantic extension for configuration

class Settings(BaseSettings):
    DATABASE_URL: str # no default
    SECRET_KEY: str # no default
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # expires after 30 mins

    model_config = SettingsConfigDict(
        env_file=".env", # to read .env file
        env_file_encoding="utf-8", # standard encoding
        extra="ignore", # other variables in .env are ignored
    )

settings = Settings() # instantiates 

# app shouldn't run w/o DB URL or signing key