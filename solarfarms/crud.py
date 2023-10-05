from sqlalchemy.orm import Session

from solarfarms import models, schemas


def get_farm(db: Session, id: int):
    return db.query(models.Farm).filter(models.Farm.id == id).first()


def create_farm(db: Session, farm: schemas.Farm):
    db_farm = models.Farm(
        name=farm.name,
        capacity_kw=farm.capacity_kw,
        address=farm.address,
        city=farm.city,
        state=farm.state,
        zip=farm.zip
    )
    db.add(db_farm)
    db.commit()
    db.refresh(db_farm)