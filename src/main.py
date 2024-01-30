import os

import validators
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.models.schemas import URLBase
from src.services.url_fetcher import fetch_data_layer

load_dotenv()

app = FastAPI()

bearer_scheme = HTTPBearer()


def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials.scheme != "Bearer":
        raise HTTPException(status_code=403, detail="Invalid scheme")

    print(credentials.credentials)
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
        return fetch_data_layer(url.target_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
