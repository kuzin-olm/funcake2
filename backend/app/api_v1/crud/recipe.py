from typing import List

from aiofiles import os

from sqlalchemy import desc, not_, and_, asc
from sqlalchemy.orm import Session

from app import models
from app.api_v1.error import NotFoundCake, InvalideCake
from app.api_v1.logic.delete_file import delete_except_current_files_from_recipe
from app.api_v1.schema.recipe import RecipeCreate, RecipeUpdate
from app.db.database import Base
from app.models import FileType


def get_all_recipes(db: Session, is_trade: bool = None) -> list[models.Recipe]:
    query = db.query(models.Recipe)
    if is_trade is not None:
        query = query.filter_by(is_trade=is_trade)
    return query.order_by(desc(models.Recipe.uuid)).all()


def get_recipe_by_id(db: Session, uuid) -> models.Recipe:
    recipe = db.query(models.Recipe).get(uuid)

    if not recipe:
        raise NotFoundCake("Отсутствует рецепт с указанным uuid")

    return recipe


def add_recipe(db: Session, recipe: RecipeCreate) -> models.Recipe:
    recipe_dict: dict = recipe.dict()
    layers = recipe_dict.pop("layers", [])

    created_recipe = models.Recipe(**recipe_dict)

    for layer in layers:
        ingredients: List[dict] = layer.pop("ingredients", [])

        created_layer = models.Layer(**layer)

        for ingredient in ingredients:
            created_consistency = models.ConsistencyIngredient(**ingredient)
            created_layer.ingredients.append(created_consistency)

        created_recipe.layers.append(created_layer)

    db.add(created_recipe)
    db.commit()
    return created_recipe


def upd_recipe(db: Session, uuid: int, new_recipe: RecipeUpdate) -> models.Recipe:
    recipe_db = get_recipe_by_id(db, uuid)

    recipe_dict = new_recipe.dict()
    recipe_uuid = recipe_dict.pop("uuid")

    # удаление дополнительных картинок
    uuids_current_images = recipe_dict.pop("uuids_current_images", [])
    delete_except_current_files_from_recipe(db, recipe_uuid, uuids_current_images, FileType.image_other)
    # удаление документов
    uuids_current_docs = recipe_dict.pop("uuids_current_docs", [])
    delete_except_current_files_from_recipe(db, recipe_uuid, uuids_current_docs, FileType.document)

    layers: List[dict] = recipe_dict.pop("layers", [])

    db.query(models.Recipe).filter_by(uuid=uuid).update(recipe_dict)

    # удаление слоев, которые отсутствуют в обновленной версии рецепта
    diff_layer_uuids = get_difference_uuids_for_deleting(recipe_db.layers, layers)
    if diff_layer_uuids:
        db.query(models.Layer).filter(models.Layer.uuid.in_(diff_layer_uuids)).delete()

    for layer in layers:
        layer_uuid = layer.pop("uuid", None)
        consistencys: List[dict] = layer.pop("ingredients", [])

        # если у слоя есть uuid, то это старый слой и его апдейтим
        if layer_uuid is not None:
            layer_db: models.Layer = db.query(models.Layer).get(layer_uuid)
            if layer_db is None:
                raise InvalideCake("Не верные данные. Не существующий uuid слоя.")

            db.query(models.Layer).filter_by(uuid=layer_uuid).update(layer)

            # удаление консистенций, которые отсутствуют в обновленной версии рецепта
            diff_consystency_uuids = get_difference_uuids_for_deleting(layer_db.ingredients, consistencys)
            if diff_consystency_uuids:
                db.query(models.ConsistencyIngredient).filter(
                    models.ConsistencyIngredient.uuid.in_(diff_consystency_uuids)
                ).delete()

            for consistency in consistencys:
                consystency_uuid = consistency.pop("uuid", None)
                if consystency_uuid is not None:
                    db.query(models.ConsistencyIngredient).filter_by(uuid=consystency_uuid).update(consistency)
                else:
                    new_consistency = models.ConsistencyIngredient(**consistency)
                    layer_db.ingredients.append(new_consistency)

        # если у слоя нет uuid, то это новый слой
        else:
            created_layer = models.Layer(**layer)
            for consistency in consistencys:
                created_consistency = models.ConsistencyIngredient(**consistency)
                created_layer.ingredients.append(created_consistency)
            recipe_db.layers.append(created_layer)

    db.commit()
    return recipe_db


async def del_recipe(db: Session, uuid: int):
    deleted_recipe = get_recipe_by_id(db, uuid)
    files = [file.path for file in deleted_recipe.files]
    db.query(models.Recipe).filter_by(uuid=uuid).delete()
    db.commit()

    for file in files:
        try:
            await os.remove(file)
        except Exception:
            ...


def get_difference_uuids_for_deleting(array_in_db: List[Base], array_new: List[dict]) -> set:
    # смотрим разницу в uuid`ах у существующего и обновленного
    uuids_db = set([each.uuid for each in array_in_db])
    uuids_upd = set([each.get("uuid") for each in array_new if each.get("uuid")])
    return uuids_db - uuids_upd
