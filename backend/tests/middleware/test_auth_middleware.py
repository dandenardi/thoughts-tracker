import pytest
from fastapi import HTTPException
from firebase_admin import auth
from unittest.mock import patch, MagicMock, AsyncMock, Mock
from app.middleware.auth_middleware import get_current_user
from backend.app.models.user import User

@pytest.fixture
def mock_firebase_user():
    return {
        "uid": "test_uid",
        "email": "test@example.com",
        "name": "Test User",
        "picture": "https://example.com/photo.jpg",
    }

@pytest.fixture
def mock_request():
    request = Mock()
    request.headers = {"Authorization": "Bearer test_token"}
    return request

@patch("firebase_admin.auth.verify_id_token")
@patch("app.services.user_service.get_user_by_firebase_uid", new_callable=AsyncMock)
@patch("app.services.user_service.create_user", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_get_current_user_existing_user(
    mock_create_user,
    mock_get_user_by_firebase_uid,
    mock_verify_id_token,
    mock_request,
    mock_firebase_user,
):
    """
    Tests if middleware returns an existing user
    """
    mock_verify_id_token.return_value = mock_firebase_user

    # 🔹 Retorna um objeto User real (não um MagicMock)
    mock_get_user_by_firebase_uid.return_value = User(
        uid=mock_firebase_user["uid"],
        email=mock_firebase_user["email"],
        name=mock_firebase_user.get("name", ""),
        photo_url=mock_firebase_user.get("picture", "")
    )
    
    user = await get_current_user(mock_request, token=MagicMock(credentials="test_token"))

    assert user.uid == mock_firebase_user["uid"]
    assert user.email == mock_firebase_user["email"]
    

@patch("firebase_admin.auth.verify_id_token", side_effect=Exception("Token inválido"))
@pytest.mark.asyncio
async def test_get_current_user_invalid_token(mock_verify_id_token, mock_request):
    """
    Tests if middleware returns an error when an invalid token is provided.
    """
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(mock_request, token=MagicMock(credentials="invalid_token"))

    assert excinfo.value.status_code == 401
    assert "Invalid or expired token" in excinfo.value.detail

@pytest.mark.asyncio
async def test_get_current_user_no_user(mock_request):
    # Arrange
    with patch('app.middleware.auth_middleware.get_user_by_firebase_uid') as mock_get_user:
        mock_get_user.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(mock_request, token=MagicMock(credentials="test_token"))
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid or expired token"
