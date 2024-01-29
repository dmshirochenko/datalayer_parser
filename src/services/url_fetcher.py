import os
import json
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

load_dotenv()

def fetch_data_layer(url, retries=3, timeout=30):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    selenium_server_url = os.getenv("SELENIUM_SERVER_URL")

    attempt = 0
    while attempt < retries:
        try:
            driver = webdriver.Remote(
                command_executor=selenium_server_url, options=options
            )
            driver.get(url)

            # Wait for the page to be fully loaded
            WebDriverWait(driver, timeout).until(lambda d: d.execute_script("return document.readyState") == "complete")

            data_layer = driver.execute_script("return JSON.stringify(window.dataLayer);")
            return json.loads(data_layer)

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2**attempt)  # Exponential backoff
            attempt += 1
        finally:
            driver.quit()

    raise Exception("Failed to fetch data layer after several retries")
