from sqlalchemy.orm import Session

from app.api_v1.crud.measure import get_all_measures
from app.api_v1.tests.seeds.measure import seed_measures


def test_getting_all_measurements(seed_measures, db: Session):
    measures = get_all_measures(db)
    assert len(measures) == 2
    measure = measures[0]
    assert measure.uuid == 1
    assert measure.name == "кг"
