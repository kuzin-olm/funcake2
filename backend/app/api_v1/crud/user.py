from sqlalchemy.orm import Session

from app import models
from app.api_v1.schema.user import UserCreate


def get_user_by_id(db: Session, id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.uuid == id).one_or_none()


def get_user_by_nickname(db: Session, nickname: str) -> models.User | None:
    return db.query(models.User).filter_by(nickname=nickname).one_or_none()


def save_user(db: Session, user: UserCreate):
    ...


def delete_user(db: Session, nickname: str):
    ...
