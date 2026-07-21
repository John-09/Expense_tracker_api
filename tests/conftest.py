import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# Ensures all model tables are registered in Base.metadata.
from app.models import Category, Expense  # noqa: F401


TEST_DATABASE_URL = "postgresql+psycopg://john:admin@localhost:5432/expense_tracker_test"

test_engine = create_engine(
    TEST_DATABASE_URL
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autocommit=False,
    autoflush=False,
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def clean_test_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()