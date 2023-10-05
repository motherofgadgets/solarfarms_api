import json

from fastapi import HTTPException
from sqlalchemy.orm import Session

from solarfarms import models, schemas


def get_farm(db: Session, farm_id: int):
    db_farm = db.query(models.Farm).filter(models.Farm.id == farm_id).first()
    if not db_farm:
        raise HTTPException(status_code=404, detail="Farm not found.")
    return db_farm


def get_farm_count(db: Session):
    return db.query(models.Farm).count()


def create_farm(db: Session, farm: schemas.Farm):
    db_farm = models.Farm(
        name=farm.name,
        capacity_kw=farm.capacity_kw,
        address=farm.address,
        city=farm.city,
        state=farm.state,
        zip=farm.zip,
    )
    db.add(db_farm)
    db.commit()
    db.refresh(db_farm)


def load_farms_bulk(db: Session):
    with open("projects.json", "r") as f:
        data = json.load(f)
    db.bulk_insert_mappings(models.Farm, data)
    db.commit()
