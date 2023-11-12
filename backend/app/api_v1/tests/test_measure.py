import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.core.config import settings
from app.models import Measure


@pytest.fixture
def seed_measures(db: Session):
    db_measures = [Measure(uuid=1, name="кг"), Measure(uuid=2, name="гр")]
    db.bulk_save_objects(db_measures)
    db.commit()


def test_list_measures(seed_measures, client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/measure")
    assert response.status_code == 200
    rsponse_data = response.json()
    assert len(rsponse_data) == 2
    measure = rsponse_data[0]
    assert measure["uuid"] == 1
    assert measure["name"] == "кг"
