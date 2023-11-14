import pytest
from sqlalchemy.orm import Session

from app.models import Recipe


@pytest.fixture
def seed_recipe(db: Session) -> Recipe:
    recipe = Recipe(
        title="title",
        description="description",
        short_description="short_description",
        recipe_text="recipe_text",
        profit=2,
        is_trade=True,
    )
    db.add(recipe)
    db.commit()
    return recipe
