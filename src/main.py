import validators
from fastapi import FastAPI, HTTPException

from src.models.schemas import URLBase
from src.services.url_fetcher import fetch_data_layer

app = FastAPI()


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@app.get("/")
def read_root():
    return "Welcome to the DataLayer Fetcher API"


from fastapi import HTTPException


@app.post("/url")
def create_url(url: URLBase):
    if not validators.url(url.target_url):
        raise HTTPException(status_code=400, detail="Your provided URL is not valid")

    try:
        return fetch_data_layer(url.target_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
