import logging.config

import validators
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.config.logger import LOGGING
from src.config.config import settings
from src.models.schemas import URLBase, DataLayerPayload
from src.services.url_fetcher import DataLayerFetcher
from src.services.dependencies import verify_api_key
from src.services.datalayer_handler import filter_datalayer, data_layer_dct_initializer
from src.db.db_connector import RedisJSONClient, get_redis_connection

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
def read_root():
    return JSONResponse(status_code=200, content={"message": "Welcome to the DataLayer Fetcher API"})


@router.get("/v1/datalayers/{partner_id}")
def get_datalayer_info(
    partner_id: str, db: RedisJSONClient = Depends(get_redis_connection), api_key: str = Depends(verify_api_key)
) -> JSONResponse:
    try:
        datalayer_info = db.get_json(partner_id)
        if not datalayer_info:
            raise HTTPException(status_code=404, detail="Data layer information not found")
        logger.info(f"Datalayer information fetched successfully for {partner_id}")
        return JSONResponse(status_code=200, content=datalayer_info, headers={'ngrok-skip-browser-warning': 'true'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/v1/datalayers")
def store_datalayer_info(
    payload: DataLayerPayload,
    db: RedisJSONClient = Depends(get_redis_connection),
    api_key: str = Depends(verify_api_key),
):
    try:
        filtered_recieved_datalayer = filter_datalayer(payload.dataLayerPayload.dataLayer)
        if filtered_recieved_datalayer:
            datalayer_info = db.get_json(payload.dataLayerPayload.partnerId)
            if datalayer_info:
                datalayer_info[payload.dataLayerPayload.selectedPage] = filtered_recieved_datalayer
            else:
                datalayer_info = data_layer_dct_initializer()
                datalayer_info[payload.dataLayerPayload.selectedPage] = filtered_recieved_datalayer

            if db.set_json(payload.dataLayerPayload.partnerId, datalayer_info):
                logger.info(f"Datalayer information stored successfully for {payload.dataLayerPayload.partnerId}")
                return JSONResponse(status_code=200, content={"message": "Data layer information stored successfully"})
            else:
                raise HTTPException(status_code=500, detail="Failed to store datalayer information")
        else:
            raise HTTPException(status_code=400, detail="Datalayer is empty or not in the correct format")
    except Exception as e:
        logger.error(f"Failed to store data layer for {payload.dataLayerPayload.partnerId}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/v1/url")
def fetch_data_layer_info(url: URLBase, api_key: str = Depends(verify_api_key)):
    if not validators.url(url.target_url):
        raise HTTPException(status_code=400, detail="Invalid URL provided")

    selenium_server_url = settings.selenium_server_url

    try:
        with DataLayerFetcher(selenium_server_url) as fetcher:
            logger.info(f"Fetching data layer for {url.target_url}")
            return JSONResponse(status_code=200, content=fetcher.fetch_data_layer(url.target_url))
    except Exception as e:
        logger.error(f"Failed to fetch data layer for {url.target_url}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
