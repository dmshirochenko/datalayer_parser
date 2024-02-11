import os
from pydantic import Field
from pydantic_settings import BaseSettings

# Assuming you've correctly set up BASE_DIR and ENV_FILE_PATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_file = "../.env"
ENV_FILE_PATH = os.path.join(BASE_DIR, env_file)


class Settings(BaseSettings):
    app_debug_level: str = Field("INFO", env="APP_DEBUG_LEVEL")
    base_dir: str = BASE_DIR
    max_wait_time: int = Field(15, env="MAX_WAIT_TIME")
    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: int = Field(6380, env="REDIS_PORT")
    redis_password: str = Field(..., env="REDIS_PASSWORD")
    redis_db: int = Field(0, env="REDIS_DB")
    selenium_server_url: str = Field(..., env="SELENIUM_SERVER_URL")
    bearer_token: str = Field(..., env="BEARER_TOKEN")

    class Config:
        env_file = ENV_FILE_PATH
        env_file_encoding = "utf-8"


settings = Settings()

unwanted_event_names = [
    "gtm.click",  # General clicks captured by GTM.
    "gtm.load",  # Page load events.
    "gtm.dom",  # DOM ready events.
    "gtm.scroll",  # Scrolling events.
    "gtm.resize",  # Browser resize events.
    "gtm.historyChange",  # History change events, often triggered by single page applications.
    "gtm.js",  # JavaScript load events.
    "gtm.noScript",  # Fires when a user has disabled JavaScript.
    "gtm.video",  # Generic video interaction events.
    "gtm.elementVisibility",  # Element visibility changes.
    "gtm.timer",  # Timer events.
    "gtm.triggerGroup",  # Trigger group events.
    "gtm.formSubmit",  # Form submission events.
    "gtm.linkClick",  # Link click events.
    "gtm.message",  # PostMessage or similar message events.
    "gtm.scrollDepth",  # Scroll depth events.
]
