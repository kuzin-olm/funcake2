from typing import List, Union

from fastapi import APIRouter, status, Depends, Body, HTTPException, Form, File, UploadFile
from fastapi_jwt_auth import AuthJWT

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, ProgrammingError

from app.api_v1.logic.delete_file import delete_prev_img_recipe
from app.db.connector import get_db
from app.api_v1.schema.recipe import Recipe, RecipeAdmin, RecipeCreate, RecipeUpdate
from app.api_v1.crud.recipe import get_all_recipes, get_recipe_by_id, add_recipe, upd_recipe, del_recipe
from app.api_v1.logic.save_file import save_prev_img_recipe, save_other_img_recipe, save_doc_recipe

router = APIRouter(prefix="/recipe", tags=["recipe"])


@router.get("", status_code=status.HTTP_200_OK, response_model=List[Recipe])
async def get_recipes(db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_optional()

    if authorize.get_jwt_subject():
        recipes = get_all_recipes(db)
    else:
        recipes = get_all_recipes(db, is_trade=True)
    return recipes


@router.get("/{uuid}", status_code=status.HTTP_200_OK)
async def get_recipe_detail(uuid: int, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_optional()

    recipe = get_recipe_by_id(db, uuid)

    if authorize.get_jwt_subject():
        recipe_data = RecipeAdmin.from_orm(recipe)
    else:
        if not recipe.is_trade:
            raise HTTPException(status_code=404, detail="Отсутствует рецепт с указанным uuid.")
        recipe_data = Recipe.from_orm(recipe)
    return recipe_data


@router.post("", status_code=status.HTTP_201_CREATED, response_model=RecipeAdmin)
async def create_recipe(recipe: RecipeCreate = Form(),
                        prev_image: UploadFile = File(None),
                        other_images: List[UploadFile] = File(None),
                        docs: List[UploadFile] = File(None),
                        db: Session = Depends(get_db),
                        authorize: AuthJWT = Depends()
                        ):
    authorize.jwt_required()

    try:
        new_recipe = add_recipe(db, recipe)
    except IntegrityError:
        raise HTTPException(status_code=422, detail="Не верные данные.")

    if prev_image:
        await save_prev_img_recipe(db, new_recipe.uuid, prev_image)
    if other_images:
        [await save_other_img_recipe(db, new_recipe.uuid, other_img) for other_img in other_images]
    if docs:
        [await save_doc_recipe(db, new_recipe.uuid, doc) for doc in docs]

    try:
        if any([prev_image, other_images, docs]):
            db.commit()
    except (IntegrityError, ProgrammingError):
        db.rollback()

    return new_recipe


@router.put("/{uuid}", status_code=status.HTTP_200_OK, response_model=RecipeAdmin)
async def update_recipe(uuid: int,
                        recipe: RecipeUpdate = Form(),
                        prev_image: UploadFile = File(None),
                        other_images: List[UploadFile] = File(None),
                        docs: List[UploadFile] = File(None),
                        db: Session = Depends(get_db),
                        authorize: AuthJWT = Depends()
                        ):
    authorize.jwt_required()

    try:
        recipe = upd_recipe(db=db, uuid=uuid, new_recipe=recipe)
    except IntegrityError:
        raise HTTPException(status_code=422, detail="Не верные данные.")

    if prev_image:
        delete_prev_img_recipe(db, recipe.uuid)
        await save_prev_img_recipe(db, recipe.uuid, prev_image)
    if other_images:
        [await save_other_img_recipe(db, recipe.uuid, other_img) for other_img in other_images]
    if docs:
        [await save_doc_recipe(db, recipe.uuid, doc) for doc in docs]

    try:
        if any([prev_image, other_images, docs]):
            db.commit()
    except (IntegrityError, ProgrammingError):
        db.rollback()

    return recipe


@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(uuid: int, db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    await del_recipe(db, uuid)
    return
