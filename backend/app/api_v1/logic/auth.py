from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from passlib.hash import pbkdf2_sha256

from app.models import User
from app.api_v1.schema.user import UserCreate, UserInDb, UserAuthenticate, UserAuthorize
from app.api_v1.crud.user import get_user_by_nickname


def user_registration(db: Session, user: UserCreate) -> UserInDb:
    if get_user_by_nickname(db=db, nickname=user.nickname):
        raise ValueError("Пользователь уже существует.")

    created_user = User(nickname=user.nickname, hashed_password=pbkdf2_sha256.hash(user.password2))
    db.add(created_user)
    db.commit()

    return UserInDb.from_orm(created_user)


def authenticate(db: Session, user: UserAuthenticate) -> UserInDb:
    user_in_db = get_user_by_nickname(db, user.nickname)
    if user_in_db is None:
        raise ValueError("Такого пользователя нет.")

    user_in_db: UserAuthorize = UserAuthorize.from_orm(user_in_db)
    if pbkdf2_sha256.verify(user.password, user_in_db.hashed_password):
        user_in_db: UserInDb = UserInDb.from_orm(user_in_db)
        return user_in_db

    else:
        raise ValueError("Неверный логин или пароль.")


def create_token(user: UserInDb, authorize: AuthJWT):
    return authorize.create_access_token(
        subject=user.nickname,
        user_claims=user.dict(include={"is_admin"}),
    )

