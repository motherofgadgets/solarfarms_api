from pydantic import BaseModel


class FarmBase(BaseModel):
    pass


class FarmCreate(FarmBase):
    pass


class Farm(FarmBase):
    id: int
    name: str
    capacity_kw: float
    address: str
    city: str
    state: str
    zip: str

    class Config:
        orm_mode = True
