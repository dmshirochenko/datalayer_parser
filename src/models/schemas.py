from typing import List, Optional

from pydantic import BaseModel, Field, Any


class URLBase(BaseModel):
    target_url: str

class DataLayerItems(BaseModel):
    dataLayer: List[Any]
    selectedPage: str
    partnerId: str = Field(..., regex="^\d+$")


