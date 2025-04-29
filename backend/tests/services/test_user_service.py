import pytest
from unittest.mock import Mock, patch
from app.services.user_service import get_user_by_firebase_uid, create_user
from backend.app.models.user import User

@pytest.fixture
def mock_neo4j_session():
    with patch('app.services.user_service.db.get_session') as mock_get_session:
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        yield mock_session

@pytest.fixture
def sample_user():
    return User(
        uid="test_uid",
        email="test@example.com",
        name="Test User",
        photo_url="https://example.com/photo.jpg"
    )

def test_get_user_by_firebase_uid_success(mock_neo4j_session, sample_user):
    # Arrange
    mock_result = Mock()
    mock_result.single.return_value = {
        "u": {
            "uid": sample_user.uid,
            "email": sample_user.email,
            "name": sample_user.name,
            "photo_url": sample_user.photo_url
        }
    }
    mock_neo4j_session.run.return_value = mock_result

    # Act
    result = get_user_by_firebase_uid(sample_user.uid)

    # Assert
    assert result is not None
    assert result.uid == sample_user.uid
    assert result.email == sample_user.email
    assert result.name == sample_user.name
    assert result.photo_url == sample_user.photo_url
    mock_neo4j_session.run.assert_called_once_with(
        "MATCH (u:User {uid: $uid}) RETURN u",
        uid=sample_user.uid
    )

def test_get_user_by_firebase_uid_not_found(mock_neo4j_session):
    # Arrange
    mock_result = Mock()
    mock_result.single.return_value = None
    mock_neo4j_session.run.return_value = mock_result

    # Act
    result = get_user_by_firebase_uid("non_existent_uid")

    # Assert
    assert result is None

def test_get_user_by_firebase_uid_error(mock_neo4j_session):
    # Arrange
    mock_neo4j_session.run.side_effect = Exception("Database error")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        get_user_by_firebase_uid("test_uid")
    assert str(exc_info.value) == "Database error"

def test_create_user_success(mock_neo4j_session, sample_user):
    # Arrange
    mock_result = Mock()
    mock_result.single.return_value = {
        "u": {
            "uid": sample_user.uid,
            "email": sample_user.email,
            "name": sample_user.name,
            "photo_url": sample_user.photo_url
        }
    }
    mock_neo4j_session.run.return_value = mock_result

    # Act
    result = create_user(sample_user)

    # Assert
    assert result is not None
    assert result.uid == sample_user.uid
    assert result.email == sample_user.email
    assert result.name == sample_user.name
    assert result.photo_url == sample_user.photo_url
    mock_neo4j_session.run.assert_called_once_with(
        """
                MERGE (u:User {uid: $uid})
                ON CREATE SET u.email = $email, u.name = $name, u.photo_url = $photo_url
                RETURN u
        """,
        uid=sample_user.uid,
        email=sample_user.email,
        name=sample_user.name,
        photo_url=sample_user.photo_url
    )

def test_create_user_error(mock_neo4j_session, sample_user):
    # Arrange
    mock_neo4j_session.run.side_effect = Exception("Database error")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        create_user(sample_user)
    assert str(exc_info.value) == "Database error" 