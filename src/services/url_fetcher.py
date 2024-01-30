import logging.config
from src.config.logger import LOGGING
from src.config.config import settings, data_layer_cache

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


from src.config.logger import LOGGING

load_dotenv()

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class DataLayerFetcher:
    def __init__(self, selenium_server_url, timeout=settings.max_wait_time):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--disable-extensions")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")

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

    def fetch_data_layer(self, url):
        if url in data_layer_cache:
            return data_layer_cache[url]

        try:
            self.driver.get(url)
            WebDriverWait(self.driver, self.timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            data_layer = self.driver.execute_script("return window.dataLayer || []")
            data_layer_cache[url] = data_layer
            logger.info(f"DataLayer fetched for {url}")
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
