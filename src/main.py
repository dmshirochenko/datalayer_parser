import logging.config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.config.logger import LOGGING
from src.api.v1 import datalayer_routes

load_dotenv()
logging.config.dictConfig(LOGGING)

app = FastAPI()

# Set up CORS to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


app.include_router(datalayer_routes.router)