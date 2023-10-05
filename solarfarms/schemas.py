from datetime import date
from pydantic import BaseModel


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
    farm_id: int
    date: date
    kw_total: float

    class Config:
        orm_mode = True
