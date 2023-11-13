from sqlalchemy.orm import Session

from app.models import Ingredient
from app.api_v1.crud.ingredient import add_ingredient, upd_ingredient, del_ingredient, get_ingredient_by_id, \
    get_all_ingredients
from app.api_v1.schema.ingredient import IngredientCreate, IngredientUpdate
from app.api_v1.tests.seeds.measure import seed_measures


def test_created_new_ingredient(seed_measures, db: Session):
    new_ingredient = IngredientCreate(name="и1", price=20, packing=4, uuid_measure=1)
    created_ingredient = add_ingredient(db=db, ingredient=new_ingredient)
    assert created_ingredient.uuid is not None
    assert created_ingredient.name == "и1"
    assert created_ingredient.price == 20
    assert created_ingredient.packing == 4
    assert created_ingredient.uuid_measure == 1

    desired_ingredient = get_ingredient_by_id(db, created_ingredient.uuid)
    assert desired_ingredient.uuid == created_ingredient.uuid

    assert len(get_all_ingredients(db)) == 1


def test_updated_ingredient(seed_measures, db: Session):
    ingredient = Ingredient(name="и1", price=20, packing=4, uuid_measure=1)
    db.add(ingredient)
    db.commit()

    upd_ingredient(db, ingredient.uuid, IngredientUpdate(name="и1", price=10, packing=4, uuid_measure=1))

    assert ingredient.name == "и1"
    assert ingredient.price == 10
    assert ingredient.packing == 4
    assert ingredient.uuid_measure == 1


def test_deleted_ingredient(seed_measures, db: Session):
    ingredient = Ingredient(name="и1", price=20, packing=4, uuid_measure=1)
    db.add(ingredient)
    db.commit()

    del_ingredient(db, ingredient.uuid)

    assert db.query(Ingredient).get(ingredient.uuid) is None
