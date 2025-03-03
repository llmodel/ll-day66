# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    LOG_FILE: str
    LOG_NAME: str
    API_KEY: str
    DATABASE_PATH: str

    class Config:
        env_file = ".env"

settings = Settings()