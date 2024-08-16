from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LLM_SERVER_URL: str = "http://localhost:8888"


settings = Settings()
