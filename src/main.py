import os
import logging.config

import validators
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.config.logger import LOGGING
from src.models.schemas import URLBase
from src.services.url_fetcher import DataLayerFetcher

load_dotenv()

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

app = FastAPI()

bearer_scheme = HTTPBearer()

selenium_server_url = os.getenv("SELENIUM_SERVER_URL")
fetcher = DataLayerFetcher(selenium_server_url)


def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials.scheme != "Bearer":
        raise HTTPException(status_code=403, detail="Invalid scheme")

    if credentials.credentials != os.getenv("BEARER_TOKEN"):
        raise HTTPException(status_code=403, detail="Invalid token")
    return credentials


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@app.get("/")
def read_root():
    return "Welcome to the DataLayer Fetcher API"


@app.post("/url")
def create_url(url: URLBase, api_key: str = Depends(verify_api_key)):
    if not validators.url(url.target_url):
        raise HTTPException(status_code=400, detail="Your provided URL is not valid")

    try:
        logger.info(f"Fetching data layer for {url.target_url}")
        return fetcher.fetch_data_layer(url.target_url)
    except Exception as e:
        logger.error(f"Failed to fetch data layer for {url.target_url}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
