import os

from pydantic import Field
from pydantic_settings import BaseSettings

# Global cache
data_layer_cache = {}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env_file = ".env"
ENV_FILE_PATH = os.path.join(BASE_DIR, env_file)


class Settings(BaseSettings):
    app_debug_level: str = Field("INFO", env="APP_DEBUG_LEVEL")
    base_dir: str = Field(BASE_DIR)
    max_wait_time: int = Field(15, env="MAX_WAIT_TIME")

    class Config:
        env_file = ENV_FILE_PATH


settings = Settings()
