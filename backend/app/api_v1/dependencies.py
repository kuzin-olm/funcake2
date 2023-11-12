from fastapi import Depends
from fastapi_jwt_auth import AuthJWT


def verify_auth(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
