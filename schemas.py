from pydantic import BaseModel
from typing import Optional


class CurrencySchema(BaseModel):
    code: str
    name: str
    quant: Optional[int]


class ValueSchema(BaseModel):
    value: str
    currency_id: Optional[float]
    percent: Optional[int] = 0
