import os
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

from app.main import app as fastapi_app
from app.db.base import Base
from app.db.session import get_db

# IMPORTANT: import models so Base.metadata knows about them
from app.models import habit  # noqa: F401
from app.models import completion  # noqa: F401

TEST_DATABASE_URL = os.getenv("DATABASE_URL_TEST")
if not TEST_DATABASE_URL:
    raise RuntimeError("DATABASE_URL_TEST is not set")

engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True, future=True)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

@pytest.fixture(scope="session", autouse=True)
def create_test_schema():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def clean_db():
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE habit_completions, habits RESTART IDENTITY CASCADE;"))
        conn.commit()
    yield

@pytest.fixture()
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    fastapi_app.dependency_overrides[get_db] = override_get_db
    with TestClient(fastapi_app) as c:
        yield c
    fastapi_app.dependency_overrides.clear()
