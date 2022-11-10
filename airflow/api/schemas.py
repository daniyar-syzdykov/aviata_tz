from datetime import datetime
import pydantic
from enum import Enum


class From(pydantic.BaseModel):
    at: str
    airport: str


class To(pydantic.BaseModel):
    at: str
    airport: str


class SearchSchema(pydantic.BaseModel):
    from_: From
    to: To


class SearchResultDetails(pydantic.BaseModel):
    items: dict
    price: float
    currency: str

    class Config:
        orm_mode = True


class SearchResutlSchema(pydantic.BaseModel):
    details: list[SearchResultDetails]

    class Config:
        orm_mode = True
