from sqlalchemy.orm import Session

from app import models


def get_all_measures(db: Session) -> list[models.Measure]:
    return db.query(models.Measure).all()
