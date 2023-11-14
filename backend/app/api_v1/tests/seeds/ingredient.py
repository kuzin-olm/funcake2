import pytest
from sqlalchemy.orm import Session

from app.models import Ingredient, Measure


@pytest.fixture
def seed_ingredients(db: Session):
    db_ingredients = [
        Ingredient(uuid=1, measure=Measure(uuid=1, name="кг"), name="ингредиент1", price=100, packing=1),
        Ingredient(uuid=2, measure=Measure(uuid=2, name="гр"), name="ингредиент2", price=20, packing=100)
    ]
    db.bulk_save_objects(db_ingredients)
    db.commit()
