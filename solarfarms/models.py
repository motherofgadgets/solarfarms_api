from sqlalchemy import Column, String, Float, Integer

from solarfarms.database import Base


class Farm(Base):

    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    capacity_kw = Column(Float)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
