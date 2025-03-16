from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.config import settings
from app.models.user import User
from app.core.security.password import get_password_hash


def test_login(db: Session, client: TestClient):
    """
    Test login endpoint.
    """
    # Create test user
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpassword"),
        is_active=True,
    )
    db.add(user)
    db.commit()

    # Test login
    response = client.post(
        f"{settings.API_V1_STR}/login",
        data={"username": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_incorrect_password(db: Session, client: TestClient):
    """
    Test login with incorrect password.
    """
    # Create test user
    user = User(
        email="test2@example.com",
        username="testuser2",
        hashed_password=get_password_hash("testpassword"),
        is_active=True,
    )
    db.add(user)
    db.commit()

    # Test login with incorrect password
    response = client.post(
        f"{settings.API_V1_STR}/login",
        data={"username": "test2@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert "detail" in response.json()


def test_login_inactive_user(db: Session, client: TestClient):
    """
    Test login with inactive user.
    """
    # Create test user
    user = User(
        email="test3@example.com",
        username="testuser3",
        hashed_password=get_password_hash("testpassword"),
        is_active=False,
    )
    db.add(user)
    db.commit()

    # Test login with inactive user
    response = client.post(
        f"{settings.API_V1_STR}/login",
        data={"username": "test3@example.com", "password": "testpassword"},
    )
    assert response.status_code == 400
    assert "detail" in response.json()
