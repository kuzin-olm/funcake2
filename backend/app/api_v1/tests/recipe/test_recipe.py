import pytest
from sqlalchemy.orm import Session

from app.models import Recipe
from app.api_v1.schema.recipe import RecipeCreate, RecipeUpdate, LayerUpdate, ConsistencyUpdate
from app.api_v1.crud.recipe import add_recipe, get_recipe_by_id, get_all_recipes, upd_recipe, del_recipe
from app.api_v1.tests.seeds.recipe import seed_recipe
from app.api_v1.tests.seeds.ingredient import seed_ingredients


def test_create_recipe(db: Session):
    new_recipe = RecipeCreate(
        title="title",
        description="description",
        short_description="short_description",
        recipe_text="recipe_text",
        profit=2,
        is_trade=True,
        layers=[],
    )
    created_recipe: Recipe = add_recipe(db=db, recipe=new_recipe)

    assert created_recipe.title == "title"
    assert created_recipe.description == "description"
    assert created_recipe.short_description == "short_description"
    assert created_recipe.recipe_text == "recipe_text"

    assert created_recipe.profit == 2
    assert created_recipe.is_trade is True
    assert len(created_recipe.layers) == 0

    desired_recipe = get_recipe_by_id(db, created_recipe.uuid)
    assert desired_recipe.uuid == created_recipe.uuid

    assert len(get_all_recipes(db)) == 1


def test_update_recipe(seed_ingredients, seed_recipe, db: Session):
    recipe = seed_recipe

    upd_title = recipe.title
    upd_description = recipe.description
    upd_short_description = recipe.short_description
    upd_recipe_text = "new_recipe_text"
    upd_profit = 3
    upd_is_tarde = False

    upd_schema = RecipeUpdate(
        uuid=recipe.uuid,
        title=upd_title,
        description=upd_description,
        short_description=upd_short_description,
        recipe_text=upd_recipe_text,
        profit=upd_profit,
        is_trade=upd_is_tarde,
        layers=[],
    )

    upd_recipe(db=db, uuid=recipe.uuid, new_recipe=upd_schema)

    assert recipe.title == upd_title
    assert recipe.description == upd_description
    assert recipe.short_description == upd_short_description
    assert recipe.recipe_text == upd_recipe_text
    assert recipe.profit == upd_profit
    assert recipe.is_trade == upd_is_tarde
    assert len(recipe.layers) == 0

    upd_schema.layers = [LayerUpdate(name="l1", diameter=10, ingredients=[])]
    upd_recipe(db=db, uuid=recipe.uuid, new_recipe=upd_schema)
    assert len(recipe.layers) == 1
    assert recipe.layers[0].uuid is not None
    assert recipe.layers[0].name == "l1"
    assert recipe.layers[0].diameter == 10
    assert len(recipe.layers[0].ingredients) == 0

    layer_0_uuid = recipe.layers[0].uuid
    upd_schema.layers = [
        LayerUpdate(uuid=layer_0_uuid, name="l1", diameter=20, ingredients=[]),
        LayerUpdate(name="l2", diameter=30, ingredients=[]),
    ]
    upd_recipe(db=db, uuid=recipe.uuid, new_recipe=upd_schema)
    assert len(recipe.layers) == 2
    assert recipe.layers[0].uuid == layer_0_uuid
    assert recipe.layers[0].name == "l1"
    assert recipe.layers[0].diameter == 20
    assert len(recipe.layers[0].ingredients) == 0
    assert recipe.layers[1] is not None
    assert recipe.layers[1] != layer_0_uuid
    assert recipe.layers[1].name == "l2"
    assert recipe.layers[1].diameter == 30
    assert len(recipe.layers[1].ingredients) == 0

    upd_schema.layers = [
        LayerUpdate(name="l1", diameter=20, ingredients=[ConsistencyUpdate(quantity=10, uuid_ingredient=1)]),
    ]
    upd_recipe(db=db, uuid=recipe.uuid, new_recipe=upd_schema)
    ingredients = recipe.layers[0].ingredients
    assert len(ingredients) == 1
    assert ingredients[0].uuid is not None
    assert ingredients[0].quantity == 10
    assert ingredients[0].uuid_ingredient == 1

    upd_schema.layers = [
        LayerUpdate(
            uuid=recipe.layers[0].uuid,
            name="l1",
            diameter=20,
            ingredients=[
                ConsistencyUpdate(uuid=ingredients[0].uuid, quantity=15, uuid_ingredient=1),
                ConsistencyUpdate(quantity=20, uuid_ingredient=2),
                ConsistencyUpdate(quantity=5, uuid_ingredient=1)
            ]
        ),
    ]
    upd_recipe(db=db, uuid=recipe.uuid, new_recipe=upd_schema)
    updated_ingredients = recipe.layers[0].ingredients
    assert len(updated_ingredients) == 3
    assert updated_ingredients[0].uuid == ingredients[0].uuid
    assert updated_ingredients[0].quantity == 15
    assert updated_ingredients[0].uuid_ingredient == 1
    assert updated_ingredients[1].uuid != updated_ingredients[0].uuid
    assert updated_ingredients[1].quantity == 20
    assert updated_ingredients[1].uuid_ingredient == 2
    assert updated_ingredients[2].uuid != updated_ingredients[1].uuid
    assert updated_ingredients[2].quantity == 5
    assert updated_ingredients[2].uuid_ingredient == 1

    upd_schema.layers = []
    upd_recipe(db=db, uuid=recipe.uuid, new_recipe=upd_schema)
    assert len(recipe.layers) == 0


@pytest.mark.asyncio
async def test_delete_recipe(seed_recipe, db: Session):
    recipe = seed_recipe
    await del_recipe(db=db, uuid=recipe.uuid)
    assert db.query(Recipe).get(recipe.uuid) is None

