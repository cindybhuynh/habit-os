# tests/conftest.py
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.session import get_db

TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL_TEST",
    "postgresql+psycopg://habitos:supersecretpassword@localhost:5432/habitos_test",
)

engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True, future=True)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

@pytest.fixture(scope="session", autouse=True)
def create_test_schema():
    # Create tables once for the test session
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def clean_db():
    # Clean rows before each test (keeps schema)
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE habits RESTART IDENTITY CASCADE;"))
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

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
