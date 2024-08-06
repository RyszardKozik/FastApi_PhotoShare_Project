import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app  # Ensure this import works correctly
from src.database.models import Base
from src.database.db import get_db

# Define the database URL for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create an engine and session for the test database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def session():
    """Fixture to create a new database session for a test."""
    Base.metadata.drop_all(bind=engine)  # Drop all tables
    Base.metadata.create_all(bind=engine)  # Create tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def client(session):
    """Fixture to create a TestClient with a database session."""
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture(scope="module")
def user():
    """Fixture for creating a user."""
    return {"login": "deadpool", "email": "deadpool@example.com", "password_checksum": "123456789"}

@pytest.fixture(scope="module")
def user_moder():
    """Fixture for creating a moderator user."""
    return {"login": "dead2pool", "email": "dead2pool@example.com", "password_checksum": "123456789"}

@pytest.fixture(scope="module")
def user_user():
    """Fixture for creating a normal user."""
    return {"login": "dead1pool", "email": "dead1pool@example.com", "password_checksum": "123456789"}
