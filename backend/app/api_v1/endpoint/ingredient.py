from typing import List

from fastapi import APIRouter, Depends, Body, status
from fastapi_jwt_auth import AuthJWT

from sqlalchemy.orm import Session

from app.db.connector import get_db
from app.api_v1.dependencies import verify_auth
from app.api_v1.schema.ingredient import Ingredient, IngredientCreate, IngredientUpdate
from app.api_v1.crud.ingredient import get_all_ingredients, get_ingredient_by_id, add_ingredient, del_ingredient, \
    upd_ingredient

router = APIRouter(
    prefix="/ingredient",
    tags=["ingredient"],
    # dependencies=[Depends(verify_auth)],
)


@router.get("", status_code=status.HTTP_200_OK, response_model=List[Ingredient])
async def get_ingredient_all(db: Session = Depends(get_db)):
    ingredients = get_all_ingredients(db=db)
    return ingredients


@router.get("/{uuid}", status_code=status.HTTP_200_OK, response_model=Ingredient)
async def get_ingredient_detail(uuid: int, db: Session = Depends(get_db)):
    ingredient = get_ingredient_by_id(db, uuid)
    return ingredient


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Ingredient)
async def create_ingredient(ingredient: IngredientCreate = Body(), db: Session = Depends(get_db)):
    created_ingredient = add_ingredient(db=db, ingredient=ingredient)
    return created_ingredient


@router.put("/{uuid}", status_code=status.HTTP_200_OK, response_model=Ingredient)
async def update_ingredient(uuid: int, ingredient: IngredientUpdate = Body(), db: Session = Depends(get_db)):
    updated_ingredient = upd_ingredient(db=db, uuid=uuid, ingredient=ingredient)
    return updated_ingredient


@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ingredient(uuid: int, db: Session = Depends(get_db)):
    del_ingredient(uuid=uuid, db=db)
    return
