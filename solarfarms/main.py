from fastapi import FastAPI

from solarfarms import models
from solarfarms.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Welcome to the Solar Farms Application!"}


@app.get("/farms/{farm_id}")
async def farms(farm_id: int):
    return {"farm": farm_id}
