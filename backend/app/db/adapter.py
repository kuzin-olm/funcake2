from app.db.database import SessionLocal
from app.api_v1.crud.template_layer import TemplateLayerService


class BaseRepoManager:
    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self) -> "BaseRepoManager":
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()

    def add(self, instance) -> None:
        self.db.add(instance)

    def rollback(self):
        self.db.rollback()

    def refresh(self, instance, attribute_names=None, with_for_update=None):
        self.db.refresh(instance, attribute_names, with_for_update)

    def commit(self) -> None:
        try:
            self.db.commit()
        except Exception as err:
            self.rollback()
            raise err


class RepoManager(BaseRepoManager):
    def __init__(self):
        super().__init__()
        self.template = TemplateLayerService(self.db)
