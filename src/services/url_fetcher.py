import logging.config
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from src.config.logger import LOGGING
from src.config.config import settings

from dotenv import load_dotenv

load_dotenv()

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class DataLayerFetcher:
    def __init__(self, selenium_server_url, timeout=settings.max_wait_time):
        options = webdriver.ChromeOptions()
        options.headless = True

        self.driver = webdriver.Remote(
            command_executor=selenium_server_url,
            options=options,
        )
        self.timeout = timeout

    def fetch_data_layer(self, url):
        try:
            self.driver.get(url)

            WebDriverWait(self.driver, self.timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            data_layer = self.driver.execute_script("return window.dataLayer || []")
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
