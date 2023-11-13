import pytest
from sqlalchemy.orm import Session

from app.models import Measure


@pytest.fixture
def seed_measures(db: Session):
    db_measures = [Measure(uuid=1, name="кг"), Measure(uuid=2, name="гр")]
    db.bulk_save_objects(db_measures)
    db.commit()
