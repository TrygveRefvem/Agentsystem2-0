from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    azure_openai_endpoint: str
    azure_openai_api_key: str
    azure_openai_deployment: str
    log_level: str = "INFO"
    env: str = "development"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
