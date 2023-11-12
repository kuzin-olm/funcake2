from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import Base

Model = TypeVar("Model", bound=Base)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class AbstractService(ABC):
    model: Type[Base]

    def __init__(self, db: Session):
        self.db: Session = db

    @abstractmethod
    def get_all(self, offset=None, limit=None) -> list["model"]: ...

    @abstractmethod
    def filter_by(self, **kwargs) -> list["model"]: ...

    @abstractmethod
    def get(self, uuid: int) -> "model" or None: ...

    @abstractmethod
    def get_or_none(self, **kwargs): ...

    @abstractmethod
    def create(self, schema: CreateSchema): ...

    @abstractmethod
    def update(self, uuid: int, schema: UpdateSchema) -> "model": ...

    @abstractmethod
    def delete(self, uuid: int) -> bool: ...


class BaseService(Generic[Model], AbstractService):
    def get_all(self, offset=None, limit=None) -> list[Model]:
        query = self.db.query(self.model)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        return query.all()

    def get_or_none(self, **kwargs) -> Model or None:
        return self.db.query(self.model).filter_by(**kwargs).one_or_none()

    def filter_by(self, **kwargs) -> list[Model]:
        return self.db.query(self.model).filter_by(**kwargs).all()

    def get(self, uuid: int, raise_exception: bool = False) -> Model or None:
        obj = self.db.query(self.model).get(uuid)

        if not obj and raise_exception:
            raise HTTPException(status_code=404, detail="Отсутствует объект с указанным uuid.")

        return obj

    def create(self, schema: CreateSchema) -> Model:
        created_object = self.model(**schema.dict())
        try:
            self.db.add(created_object)
            self.db.commit()
            self.db.refresh(created_object)
            return created_object

        except Exception as err:
            self.db.rollback()
            raise err

    def update(self, uuid: int, schema: UpdateSchema) -> Model:
        instance = self.get(uuid, raise_exception=True)
        self.db.query(self.model).filter_by(uuid=uuid).update(schema.dict(exclude={"uuid"}))
        try:
            self.db.commit()
            self.db.refresh(instance)
            return instance
        except Exception as err:
            self.db.rollback()
            raise err

    def delete(self, uuid: int) -> None:
        self.get(uuid, raise_exception=True)

        try:
            self.db.query(self.model).filter_by(uuid=uuid).delete()
            self.db.commit()

        except Exception as err:
            self.db.rollback()
            raise err
