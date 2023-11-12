from app.models import Layer, ConsistencyIngredient
from app.api_v1.error import NotFoundCake
from app.api_v1.crud.base import BaseService
from app.api_v1.crud.recipe import get_difference_uuids_for_deleting
from app.api_v1.schema.template_layer import TemplateLayerCreate, TemplateLayerUpdate


class TemplateLayerService(BaseService[Layer]):
    model = Layer

    def get_all(self, offset=None, limit=None) -> list[Layer]:
        return super().filter_by(is_template=True)

    def create(self, schema: TemplateLayerCreate) -> Layer:
        template: dict = schema.dict()
        ingredients: list[dict] = template.pop("ingredients", [])

        created_template = Layer(name=template["name"], is_template=True)

        for ingredient in ingredients:
            created_consistency = ConsistencyIngredient(
                uuid_ingredient=ingredient["uuid_ingredient"],
                quantity=ingredient["quantity"],
            )
            created_template.ingredients.append(created_consistency)

        self.db.add(created_template)

        try:
            self.db.commit()
            self.db.refresh(created_template)
            return created_template

        except Exception as err:
            self.db.rollback()
            raise err

    def update(self, uuid: int, schema: TemplateLayerUpdate) -> Layer:
        template_db = self.get(uuid, raise_exception=True)
        template_db.name = schema.name

        template: dict = schema.dict()
        consistencies: list[dict] = template.pop("ingredients", [])

        # удаление консистенций, которые отсутствуют в обновленной версии
        diff_consystency_uuids = get_difference_uuids_for_deleting(template_db.ingredients, consistencies)
        if diff_consystency_uuids:
            self.db.query(ConsistencyIngredient).filter(ConsistencyIngredient.uuid.in_(diff_consystency_uuids)).delete()

        for consistency in consistencies:
            consystency_uuid = consistency.pop("uuid", None)
            if consystency_uuid is not None:
                self.db.query(ConsistencyIngredient).filter_by(uuid=consystency_uuid).update(consistency)
            else:
                new_consistency = ConsistencyIngredient(**consistency)
                template_db.ingredients.append(new_consistency)

        try:
            self.db.commit()
            self.db.refresh(template_db)
            return template_db
        except Exception as err:
            raise err

    def delete(self, uuid: int) -> None:
        layer = self.get(uuid, raise_exception=True)

        if not layer.is_template:
            raise NotFoundCake("Отсутствует шаблон с указанным uuid.")

        try:
            self.db.query(self.model).filter_by(uuid=uuid).delete()
            self.db.commit()

        except Exception as err:
            self.db.rollback()
            raise err
