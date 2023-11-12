from typing import Type, Callable

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api_v1.crud.base import BaseService
from app.db.adapter import RepoManager
from app.db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_service(service: Type[BaseService]) -> Callable:
    def get_init_service(db: Session = Depends(get_db)) -> BaseService:
        return service(db)
    return get_init_service


def get_repo() -> RepoManager:
    with RepoManager() as repo:
        yield repo
