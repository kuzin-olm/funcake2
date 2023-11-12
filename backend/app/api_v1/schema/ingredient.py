from app.api_v1.schema.base import CamelModel
from app.api_v1.schema.measure import Measure


class IngredientCreate(CamelModel):
    name: str
    price: float
    packing: float
    uuid_measure: int


class Ingredient(CamelModel):
    uuid: int
    name: str
    price: float
    packing: float
    measure: Measure

    class Config:
        orm_mode = True


class IngredientUpdate(CamelModel):

    name: str
    price: float
    packing: float
    uuid_measure: int
