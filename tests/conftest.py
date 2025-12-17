from fastapi.testclient import TestClient
from main import app
import pytest
import uuid
from database import SessionLocal
from models import User
from routers.auth import create_access_token

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(scope="function")
def create_user_and_token(client):
    # create a user directly in the DB to avoid bcrypt/passlib issues in tests
    unique = uuid.uuid4().hex[:8]
    email = f"testuser_{unique}@example.com"
    db = SessionLocal()
    try:
        new_user = User(full_name="Test User", email=email, phone="+549111111111", password_hash="testhash")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user = {"id": new_user.id, "email": new_user.email, "full_name": new_user.full_name}
    finally:
        db.close()

    # create token using app's create_access_token util
    token = create_access_token({"sub": str(user["id"])})
    headers = {"Authorization": f"Bearer {token}"}
    return {"client": client, "token": token, "headers": headers, "user": user}
