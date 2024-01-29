# shortener_app/schemas.py

from pydantic import BaseModel


class URLBase(BaseModel):
    target_url: str
