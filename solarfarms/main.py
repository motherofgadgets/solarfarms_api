from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session
from typing import List

from solarfarms import crud, models, schemas
from solarfarms.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    """
    Obtains an independent database connection. Allows dependency override.
    :return: A database session that is closed when a request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    """
    Allows the app to populate the database if empty.
    """
    db = SessionLocal()
    try:
        if crud.get_farm_count(db) == 0:
            crud.load_farms_bulk(db)
        if crud.get_daily_energy_count(db) == 0:
            crud.load_daily_energy(db)
    finally:
        db.close()


@app.get("/")
async def root():
    """
    A basic message when no other endpoints are specified
    """
    return {"message": "Welcome to the Solar Farms Application!"}


@app.get(
    "/farms/{farm_id}",
    response_model=schemas.Farm,
    responses={404: {"detail": "Farm not found."}},
)
async def get_farm_by_id(farm_id: int, db: Session = Depends(get_db)):
    """
    Returns the Farm based on its ID
    :param farm_id: The numeric Farm ID
    :param db: database connection
    :return: The details for the Farm selected
    """
    return crud.get_farm(db, farm_id)


@app.get(
    "/farms/",
    response_model=List[schemas.Farm],
    responses={404: {"detail": "Farm not found."}},
)
async def filter_farms(
    state: str = Query(None, min_length=2, max_length=2, regex="^[a-zA-Z]{2}$"),
    min_capacity: float = Query(None),
    max_capacity: float = Query(None),
    db: Session = Depends(get_db),
):
    """
    Can filter all Farms based on State, OR based on the farm's capacity
    :param state: 2-letter abbreviation for state
    :param min_capacity: minimum capacity value
    :param max_capacity: maximum capacity value
    :param db: database connection
    :return: A list of filtered Farms
    """
    if state:
        return crud.get_farms_by_state(db, state.upper())
    if min_capacity is not None or max_capacity is not None:
        return crud.get_farms_by_capacity_range(db, min_capacity, max_capacity)


@app.get("/farms/{farm_id}/maxmonth/", response_model=schemas.MaxMonth)
async def get_farm_max_month(farm_id: int, db: Session = Depends(get_db)):
    """
    Calculates the total energy generated per month and returns the month with the highest total
    :param farm_id: The numeric Farm ID
    :param db: database connection
    :return: The month with the highest energy generated total.
    """
    db_farm = crud.get_farm_max_month(db, farm_id)
    return db_farm
