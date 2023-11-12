import re
from itertools import groupby
from typing import List, Optional, Dict, Any, Type

from humps.camel import case
from pydantic import validator, Field

from app.api_v1.mixin.schema_mixin import ORJSONParserMixin
from app.api_v1.schema.base import CamelModel
from app.api_v1.schema.ingredient import Ingredient
from app.core.config import settings
from app.models import FileType


class File(CamelModel):
    uuid: int
    path: str = Field(alias='url')
    type: FileType

    class Config:
        orm_mode = True

    @validator("path")
    def get_path(cls, v, values, **kwargs):
        return re.sub(f"{settings.STATIC_DIR}", settings.STATIC_URL, v)


class Recipe(CamelModel):
    uuid: int
    title: str
    description: Optional[str]
    short_description: Optional[str]
    is_trade: bool
    files: List[File] = []

    class Config:
        orm_mode = True

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        representation = super().dict(*args, **kwargs)
        self._restruct_files(representation, only_preview=True)
        return representation

    @staticmethod
    def _restruct_files(representation: dict, only_preview: bool = True):
        files = dict()
        representation["files"].sort(key=lambda f: f["type"].value)
        for key, group in groupby(representation["files"], lambda f: f["type"]):
            _group = list(group)
            if key == FileType.image_preview and _group:
                files[case(key.value)] = _group[0]
            elif key == FileType.image_other:
                files[case(key.value)] = _group
            elif not only_preview:
                files[case(key.value)] = _group
        representation.pop("files", None)
        representation.update(files)


class Consistency(CamelModel):
    uuid: int
    quantity: float
    ingredient: Ingredient

    class Config:
        orm_mode = True


class Layer(CamelModel):
    uuid: int
    name: str
    diameter: float
    is_template: bool
    ingredients: Optional[List[Consistency]] = []

    class Config:
        orm_mode = True


class RecipeAdmin(Recipe):
    recipe_text: str
    profit: float
    layers: List[Layer] = []

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        representation = super(CamelModel, self).dict(*args, **kwargs)
        self._make_shopping_list_and_update_cost(representation)
        self._restruct_files(representation, only_preview=False)
        return representation

    @staticmethod
    def _make_shopping_list_and_update_cost(representation: dict):
        total_cost = 0
        total_qty = 0
        shopping_list = []

        for layer in representation["layers"]:
            [
                shopping_list.append({
                    **ingredient["ingredient"],
                    "quantity": ingredient["quantity"]
                })
                for ingredient in layer["ingredients"]
            ]

            cost = sum([
                ingredient["quantity"] * ingredient["ingredient"]["price"] / ingredient["ingredient"]["packing"]
                for ingredient in layer["ingredients"]
            ])
            cost = round(cost, 2)

            qty = sum([ingredient["quantity"] for ingredient in layer["ingredients"]])

            total_cost += cost
            total_qty += qty

            layer.update({"cost": cost})

        # группировка ингредиентов из слоев по названию
        shopping_list = sorted(shopping_list, key=lambda x: x["name"])
        groups = groupby(shopping_list.copy(), key=lambda x: x["name"])
        shopping_list.clear()

        for key, group in groups:
            group = list(group)

            qty = sum([item["quantity"] for item in group])
            packing = group[0]["packing"]
            price = group[0]["price"]
            shop_qty = int(round(qty / packing + 0.4999))

            shopping_list.append({
                "name": key,
                "quantity": qty,
                "packing": packing,
                "measure": group[0]["measure"]["name"],
                "shopQty": shop_qty,
                "price": shop_qty * price,
            })

        representation.update({
            "totalCost": total_cost,
            "totalQty": total_qty,
            "shoppingList": shopping_list,
            "shoppingListCost": sum([each["price"] for each in shopping_list]),
        })

# ------------------------------ create sсhemas ------------------------------


class ConsistencyCreate(CamelModel):
    quantity: float
    uuid_ingredient: int


class LayerCreate(CamelModel):
    name: str
    diameter: float
    ingredients: List[ConsistencyCreate]


class RecipeCreate(ORJSONParserMixin, CamelModel):
    title: str
    description: str
    short_description: str
    recipe_text: str
    profit: float
    is_trade: bool
    layers: List[LayerCreate]


# ------------------------------ update sсhemas ------------------------------


class ConsistencyUpdate(CamelModel):
    uuid: Optional[int]
    quantity: float
    uuid_ingredient: int


class LayerUpdate(CamelModel):
    uuid: Optional[int]
    name: str
    diameter: float
    ingredients: List[ConsistencyUpdate]


class RecipeUpdate(ORJSONParserMixin, CamelModel):
    uuid: int
    title: str
    description: str
    short_description: str
    recipe_text: str
    profit: float
    is_trade: bool
    layers: List[LayerUpdate]

    uuids_current_images: List[int] = []
    uuids_current_docs: List[int] = []

