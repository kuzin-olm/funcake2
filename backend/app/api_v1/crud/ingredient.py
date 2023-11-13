from sqlalchemy.orm import Session

from app import models
from app.api_v1.error import NotFoundCake, InvalideCake
from app.api_v1.schema.ingredient import IngredientCreate, IngredientUpdate


def get_all_ingredients(db: Session) -> list[models.Ingredient]:
    return db.query(models.Ingredient).order_by(models.Ingredient.name).all()


def get_ingredient_by_id(db: Session, uuid) -> models.Ingredient:
    ingredient = db.query(models.Ingredient).get(uuid)

    if not ingredient:
        raise NotFoundCake("Отсутствует ингредиент с указанным uuid.")

    return ingredient


def add_ingredient(db: Session, ingredient: IngredientCreate) -> models.Ingredient:
    created_ingredient = models.Ingredient(**ingredient.dict())
    db.add(created_ingredient)
    db.commit()
    return created_ingredient


def upd_ingredient(db: Session, uuid: int, ingredient: IngredientUpdate) -> models.Ingredient:
    ingredient_in_db = get_ingredient_by_id(db, uuid)
    db.query(models.Ingredient).filter_by(uuid=uuid).update(ingredient.dict())
    db.commit()
    return ingredient_in_db


def del_ingredient(db: Session, uuid: int):
    deleted_ingredient = get_ingredient_by_id(db, uuid)
    if deleted_ingredient.consistency:
        raise InvalideCake("Ингредиент с указанным uuid, не может быть удален, т.к. используется в рецепте(ах).")

    db.delete(deleted_ingredient)
    db.commit()
    return deleted_ingredient
