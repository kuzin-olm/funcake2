from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import SessionLocal, Base
from app.models import Measure


measures = [
    Measure(uuid=1, name="кг"),
    Measure(uuid=2, name="г"),
    Measure(uuid=3, name="л"),
    Measure(uuid=4, name="мл"),
    Measure(uuid=5, name="шт"),
    Measure(uuid=6, name="м"),
]


def load(data: list[Base]):
    db: Session = SessionLocal()
    try:
        for each in data:
            db.add(each)
            try:
                db.commit()
            except IntegrityError:
                db.rollback()

        db.execute("SELECT setval(pg_get_serial_sequence('measure', 'uuid'), max(uuid)) FROM measure;")
    finally:
        db.close()


if __name__ == "__main__":
    load(measures)
