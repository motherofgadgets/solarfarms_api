import json

from fastapi import HTTPException
from sqlalchemy.orm import Session

from solarfarms import models


def get_farm(db: Session, farm_id: int):
    db_farm = db.query(models.Farm).filter(models.Farm.id == farm_id).first()
    if not db_farm:
        raise HTTPException(status_code=404, detail="Farm not found.")
    return db_farm


def get_farm_count(db: Session):
    return db.query(models.Farm).count()


def get_farms_by_state(db: Session, state: str):
    db_farms = db.query(models.Farm).filter(models.Farm.state == state).all()
    if not db_farms:
        raise HTTPException(status_code=404, detail="Farm not found.")
    return db_farms


def load_farms_bulk(db: Session):
    with open("projects.json", "r") as f:
        data = json.load(f)
    db.bulk_insert_mappings(models.Farm, data)
    db.commit()
