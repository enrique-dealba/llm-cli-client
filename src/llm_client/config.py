import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LLM_SERVER_URL: str = os.environ.get("LLM_SERVER_URL", "http://localhost:8888")


settings = Settings()
