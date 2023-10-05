from fastapi import Depends, FastAPI
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
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Welcome to the Solar Farms Application!"}


@app.get("/farms/{farm_id}", responses={404: {"detail": "Farm not found."}})
async def farms(farm_id: int, db: Session = Depends(get_db)):
    return crud.get_farm(db, farm_id)
