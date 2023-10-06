from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session

from solarfarms import crud, models
from solarfarms.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
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
    return {"message": "Welcome to the Solar Farms Application!"}


@app.get("/farms/{farm_id}", responses={404: {"detail": "Farm not found."}})
async def get_farm_by_id(farm_id: int, db: Session = Depends(get_db)):
    return crud.get_farm(db, farm_id)


@app.get("/farms/")
async def filter_farms(
    state: str = Query(None),
    min_capacity: float = Query(None),
    max_capacity: float = Query(None),
    db: Session = Depends(get_db),
):
    if state:
        return crud.get_farms_by_state(db, state)
    if min_capacity is not None or max_capacity is not None:
        return crud.get_farms_by_capacity_range(db, min_capacity, max_capacity)


@app.get("/farms/{farm_id}/maxmonth/")
async def get_farm_max_month(farm_id: int, db: Session = Depends(get_db)):
    db_farm = crud.get_farm_max_month(db, farm_id)
    return db_farm
