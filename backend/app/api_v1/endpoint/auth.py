from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, Body, status, Form
from fastapi_jwt_auth import AuthJWT
from starlette.responses import JSONResponse

from app.core.config import settings
from app.db.connector import get_db
from app.api_v1.schema.user import UserCreate, UserInDb, UserAuthenticate
from app.api_v1.logic.auth import user_registration, authenticate, create_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user(authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    is_admin = authorize.get_raw_jwt()["is_admin"]
    return {"user": current_user, "isAdmin": is_admin}


@router.post('/login', status_code=status.HTTP_200_OK)
async def authenticate_user(user: UserAuthenticate = Form(), authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        user_in_db: UserInDb = authenticate(db, user)
        token = create_token(user_in_db, authorize)
        return {"accessToken": token}

    except Exception as err:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(err)})


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_new_user(user: UserCreate = Form(), authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    if not settings.USERS_OPEN_REGISTRATION:
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={"detail": "Регистрация временно недоступна."}
        )

    try:
        user_in_db: UserInDb = user_registration(db, user)
        token = create_token(user_in_db, authorize)
        return {"accessToken": token}

    except Exception as err:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": str(err)})
