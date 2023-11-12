from typing import Optional, List

from app.api_v1.schema.base import CamelModel
from app.api_v1.schema.ingredient import Ingredient


class TemplateConsistency(CamelModel):
    uuid: int
    quantity: float
    ingredient: Ingredient

    class Config:
        orm_mode = True


class TemplateLayer(CamelModel):
    uuid: int
    name: str
    is_template: bool
    ingredients: Optional[List[TemplateConsistency]] = []

    class Config:
        orm_mode = True


class TemplateConsistencyCreate(CamelModel):
    quantity: float
    uuid_ingredient: int


class TemplateLayerCreate(CamelModel):
    name: str
    ingredients: List[TemplateConsistencyCreate]


class TemplateConsistencyUpdate(TemplateConsistencyCreate):
    uuid: Optional[int]


class TemplateLayerUpdate(TemplateLayerCreate):
    ingredients: List[TemplateConsistencyUpdate]
