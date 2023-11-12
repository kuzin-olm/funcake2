import pytest
from fastapi.testclient import TestClient
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from app.core.config import settings
from app.db.connector import get_db
from app.main import app
from app.models import Base


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI_TEST)
    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function", name="db")
def get_test_db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    db = Session(bind=connection)
    yield db
    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    token = AuthJWT().create_access_token(subject="tester")

    with TestClient(app) as _client:
        _client.headers.update({"Authorization": f"Bearer {token}"})
        yield _client
