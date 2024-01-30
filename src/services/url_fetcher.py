import os
import json
import time
import logging.config
from functools import lru_cache
from src.config.logger import LOGGING

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from src.config.logger import LOGGING

load_dotenv()

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class DataLayerFetcher:
    def __init__(self, selenium_server_url, timeout=30):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Disable images and CSS
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.managed_default_content_settings.stylesheet": 2,
        }
        options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Remote(
            command_executor=selenium_server_url,
            options=options,
        )
        self.timeout = timeout

    @lru_cache(maxsize=16)
    def fetch_data_layer(self, url):
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, self.timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            data_layer = self.driver.execute_script("return window.dataLayer || []")
            return data_layer
        except Exception as e:
            logger.error(f"Attempt failed: {e}")
            return None

    def close(self):
        try:
            self.driver.quit()
        except Exception as e:
            logger.error(f"Failed to close the driver: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
