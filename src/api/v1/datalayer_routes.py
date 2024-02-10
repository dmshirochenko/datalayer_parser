import os
import logging

import validators
from fastapi import APIRouter, Depends, HTTPException

from src.models.schemas import URLBase, DataLayerPayload
from src.services.url_fetcher import DataLayerFetcher
from src.services.dependencies import verify_api_key, raise_bad_request
from src.services.datalayer_handler import filter_datalayer
from src.db.db_connector import RedisJSONClient, get_redis_connection

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
def read_root():
    return "Welcome to the DataLayer Fetcher API"


@router.post("/v1/datalayers")
def store_datalayer_info(
    payload: DataLayerPayload,
    db: RedisJSONClient = Depends(get_redis_connection),
    api_key: str = Depends(verify_api_key),
):
    try:
        filtered_data_layer = filter_datalayer(payload.dataLayerPayload.dataLayer)
        if filtered_data_layer:
            print(filtered_data_layer)
            db.set_json("partner_id_1", {"dataLayer": filtered_data_layer})
            retrieved_user_info = db.get_json("partner_id_1")
            print(retrieved_user_info)
        else:
            raise_bad_request("Your provided datalayer is not empty or not in the correct format")
    except Exception as e:
        logger.error(f"Failed to store data layer for {payload}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    return "OK"


@router.post("/v1/url")
def fetch_data_layer_info(url: URLBase, api_key: str = Depends(verify_api_key)):
    if not validators.url(url.target_url):
        raise_bad_request("Your provided URL is not valid")

    selenium_server_url = os.getenv("SELENIUM_SERVER_URL")

    try:
        with DataLayerFetcher(selenium_server_url) as fetcher:
            logger.info(f"Fetching data layer for {url.target_url}")
            return fetcher.fetch_data_layer(url.target_url)
    except Exception as e:
        logger.error(f"Failed to fetch data layer for {url.target_url}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
