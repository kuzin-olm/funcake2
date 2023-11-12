from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from app.core.config import settings
from app.core.logger import init_logging
from app.core.jwt_config import JWTSettings
from app.api_v1.api import api_router
from app.api_v1.error import ErrorCake

init_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url=f"{settings.API_V1_STR}/docs",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

if settings.DEBUG:
    app.mount(settings.STATIC_URL, StaticFiles(directory=settings.STATIC_DIR), name=settings.STATIC_ROOT)


@AuthJWT.load_config
def get_config():
    return JWTSettings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=401, content={"detail": exc.message})


async def handle_cake_error(request: Request, exc: ErrorCake):
    return JSONResponse(status_code=exc.status, content=dict(detail=exc.message))


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(ErrorCake, handle_cake_error)

app.include_router(api_router, prefix=settings.API_V1_STR)
