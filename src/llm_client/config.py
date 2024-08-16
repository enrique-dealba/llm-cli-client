import json
from pathlib import Path

from pydantic_settings import BaseSettings

CONFIG_FILE = Path.home() / ".llm_client_config.json"


def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


class Settings(BaseSettings):
    LLM_SERVER_URL: str = "http://localhost:8888"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        config = load_config()
        if "LLM_SERVER_URL" in config:
            self.LLM_SERVER_URL = config["LLM_SERVER_URL"]


settings = Settings()
