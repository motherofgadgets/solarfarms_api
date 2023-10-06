import csv
import os
import json

from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import func, extract
from sqlalchemy.orm import Session

from solarfarms import models


def get_farm(db: Session, farm_id: int):
    db_farm = db.query(models.Farm).filter(models.Farm.id == farm_id).first()
    if not db_farm:
        raise HTTPException(status_code=404, detail="Farm not found.")
    return db_farm


def get_farm_count(db: Session):
    return db.query(models.Farm).count()


def get_daily_energy_count(db: Session):
    return db.query(models.DailyEnergy).count()


def get_farms_by_state(db: Session, state: str):
    db_farms = db.query(models.Farm).filter(models.Farm.state == state).all()
    if not db_farms:
        raise HTTPException(status_code=404, detail="Farm not found.")
    return db_farms


def get_farms_by_capacity_range(db: Session, min_capacity: float, max_capacity: float):
    db_farms = db.query(models.Farm)
    if min_capacity is not None and max_capacity is not None:
        if min_capacity >= max_capacity:
            raise HTTPException(
                status_code=400, detail="min_capacity should be less than max_capacity"
            )
    if min_capacity is not None:
        db_farms = db_farms.filter(models.Farm.capacity_kw >= min_capacity)
    if max_capacity is not None:
        db_farms = db_farms.filter(models.Farm.capacity_kw <= max_capacity)
    results = db_farms.all()
    if not results:
        raise HTTPException(status_code=404, detail="Farms not found.")
    return results


def get_farm_max_month(db: Session, farm_id: int):
    results = (
        db.query(
            extract("year", models.DailyEnergy.date).label("year"),
            extract("month", models.DailyEnergy.date).label("month"),
            func.sum(models.DailyEnergy.kw_total).label("month_total"),
        )
        .filter(models.DailyEnergy.farm_id == farm_id)
        .group_by(
            extract("year", models.DailyEnergy.date),
            extract("month", models.DailyEnergy.date),
        )
        .order_by(func.sum(models.DailyEnergy.kw_total).desc())
        .first()
    )

    if results:
        year, month, month_total = results
        return {"year": year, "month": month, "month_total": month_total}
    else:
        raise HTTPException(status_code=404, detail="No data available")


def load_farms_bulk(db: Session):
    with open("projects.json", "r") as f:
        data = json.load(f)
    db.bulk_insert_mappings(models.Farm, data)
    db.commit()


def load_daily_energy(db: Session):
    for filename in os.listdir("generation_data"):
        farm_id = int(filename.split("_")[0])
        with open("generation_data/{}".format(filename), mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                new_daily_energy = models.DailyEnergy(
                    farm_id=farm_id,
                    date=datetime.fromisoformat(row.get("ts")).date(),
                    kw_total=row.get("total", row.get("Generation Meter RM - 01")),
                )
                db.add(new_daily_energy)
            db.commit()
