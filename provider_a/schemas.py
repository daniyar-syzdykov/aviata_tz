from datetime import datetime
import pydantic
from enum import Enum

class Airport(Enum):
    NQZ = 'NQZ'
    SCO = 'SCO'
    DME = 'DME'
    SVO = 'SVO'
    IST = 'IST'
    URA = 'URA'
    CIT = 'CIT'
    TAS = 'TAS'
    AKX = 'AKX'
    ALA = 'ALA'

class From(pydantic.BaseModel):
    at: datetime
    airport: Airport


class To(pydantic.BaseModel):
    at: datetime
    airport: Airport


class SearchSchema(pydantic.BaseModel):
    from_: From
    to: To
