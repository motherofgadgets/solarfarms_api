from datetime import date
from pydantic import BaseModel, Field
from typing import Optional


class Farm(BaseModel):
    id: int
    name: str
    capacity_kw: float
    address: str
    city: str
    state: str
    zip: str

    class Config:
        orm_mode = True


class DailyEnergy(BaseModel):
    id: Optional[int] = Field(default=None)
    farm_id: int
    date: date
    kw_total: float

    class Config:
        orm_mode = True


class MaxMonth(BaseModel):
    year: int
    month: int
    month_total: float
