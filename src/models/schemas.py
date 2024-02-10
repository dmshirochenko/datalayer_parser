from typing import List, Any

from pydantic import BaseModel, Field


class URLBase(BaseModel):
    target_url: str


class DataLayerItems(BaseModel):
    dataLayer: List[Any]
    selectedPage: str
    partnerId: str = Field(..., pattern="^\d+$")


class DataLayerPayload(BaseModel):
    dataLayerPayload: DataLayerItems
