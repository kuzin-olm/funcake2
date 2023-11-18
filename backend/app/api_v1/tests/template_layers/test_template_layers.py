from copy import copy

from sqlalchemy.orm import Session

from app.models import Layer, ConsistencyIngredient
from app.api_v1.crud.template_layer import TemplateLayerService
from app.api_v1.schema.template_layer import (
    TemplateLayerCreate,
    TemplateConsistencyCreate,
    TemplateLayerUpdate,
    TemplateConsistencyUpdate,
)
from app.api_v1.tests.seeds.ingredient import seed_ingredients


def test_create_template(seed_ingredients, db: Session):
    service = TemplateLayerService(db=db)

    schema_ingredient = TemplateConsistencyCreate(quantity=10, uuid_ingredient=1)
    schema = TemplateLayerCreate(
        name="template name 1",
        ingredients=[
            schema_ingredient,
        ],
    )

    created_template = service.create(schema)

    assert created_template.uuid is not None
    assert isinstance(created_template, Layer) is True
    assert created_template.name == schema.name
    assert len(created_template.ingredients) == 1
    consistency = created_template.ingredients[0]
    assert consistency.uuid is not None
    assert consistency.quantity == schema_ingredient.quantity
    assert consistency.uuid_ingredient == schema_ingredient.uuid_ingredient


def test_update_template(seed_ingredients, db: Session):
    service = TemplateLayerService(db=db)

    schema = TemplateLayerCreate(
        name="template name 1",
        ingredients=[
            TemplateConsistencyCreate(quantity=10, uuid_ingredient=1),
        ],
    )
    template_current = service.create(schema)
    uuid = copy(template_current.uuid)
    uuid_consistency = copy(template_current.ingredients[0].uuid)

    service.update(uuid, TemplateLayerUpdate(name="test", ingredients=[TemplateConsistencyUpdate(uuid=uuid_consistency, quantity=5, uuid_ingredient=2)]))
    assert template_current.name == "test"
    assert len(template_current.ingredients) == 1
    assert template_current.ingredients[0].uuid == uuid_consistency
    assert template_current.ingredients[0].uuid_ingredient == 2

    service.update(uuid, TemplateLayerUpdate(name="new name", ingredients=[]))
    assert template_current.name == "new name"
    assert len(template_current.ingredients) == 0


def test_delete_template(seed_ingredients, db: Session):
    template_layer = Layer(name='name', is_template=True)
    template_layer.ingredients.append(ConsistencyIngredient(quantity=5, uuid_ingredient=2))
    db.add(template_layer)
    db.commit()

    service = TemplateLayerService(db=db)
    service.delete(template_layer.uuid)
    assert service.get(template_layer.uuid) is None
