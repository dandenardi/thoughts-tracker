import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock
from firebase_admin.auth import UserRecord

client = TestClient(app)

@pytest.fixture
def mock_firebase_user():
    mock_user = MagicMock(spec=UserRecord)
    # Agora você define os atributos esperados para o mock
    mock_user.uid = "test_uid"
    mock_user.email = "test@example.com"
    mock_user.display_name = "Test User"
    mock_user.photo_url = "https://example.com/photo.jpg"
    return mock_user

@pytest.fixture
def mock_id_token():
    return "mock_valid_token"

@patch("app.services.auth_service.auth.verify_id_token")
@patch("app.services.auth_service.auth.get_user")
def test_verify_token(mock_get_user, mock_verify_id_token, mock_firebase_user, mock_id_token):
    mock_verify_id_token.return_value = {"uid": "test_uid"}
    mock_get_user.return_value=mock_firebase_user

    response = client.get("/auth/verify-token", params={"id_token": mock_id_token})

    assert response.status_code == 200
    data = response.json()

    assert data["uid"] == "test_uid"
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert data["photo_url"] == "https://example.com/photo.jpg"

@patch("app.services.auth_service.auth.verify_id_token", side_effect=Exception("Invalid token"))
def test_verify_token_invalid(mock_verify_id_token):
    response = client.get("/auth/verify-token", params={"id_token": "invalid_token"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials"



