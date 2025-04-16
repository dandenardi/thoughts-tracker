import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.services.emotion_service import add_emotion, get_all_emotions_from_db

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_neo4j_session():
    with patch('app.services.emotion_service.db.get_session') as mock_get_session:
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        yield mock_session

def test_add_emotion(mock_neo4j_session):
    # Arrange
    mock_result = Mock()
    mock_result.single.return_value = {
        "e": {
            "id": "test_id",
            "name": "Test Emotion",
            "description": "Test Description"
        }
    }
    mock_neo4j_session.run.return_value = mock_result

    # Act
    result = add_emotion("Test Emotion", "Test Description")

    # Assert
    assert result is not None
    assert result.id == "test_id"
    assert result.name == "Test Emotion"
    mock_neo4j_session.run.assert_called_once()

def test_get_all_emotions(mock_neo4j_session):
    # Arrange
    mock_results = [
        {
            "e": {
                "id": "test_id_1",
                "name": "Test Emotion 1",
                "description": "Test Description 1"
            }
        },
        {
            "e": {
                "id": "test_id_2",
                "name": "Test Emotion 2",
                "description": "Test Description 2"
            }
        }
    ]
    mock_neo4j_session.run.return_value = mock_results

    # Act
    results = get_all_emotions_from_db()

    # Assert
    assert len(results) == 2
    assert results[0].id == "test_id_1"
    assert results[1].id == "test_id_2"

