from sqlalchemy import Column, ForeignKey, String, Float, Integer, Date
from sqlalchemy.orm import relationship

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

    daily_energy = relationship("DailyEnergy", back_populates="farm")


class DailyEnergy(Base):

    __tablename__ = "daily_energy"

    id = Column(Integer, primary_key=True)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    date = Column(Date)
    kw_total = Column(Float)

    farm = relationship("Farm", back_populates="daily_energy")
