import pytest
from datetime import datetime, UTC
from unittest.mock import Mock, patch
from app.services.emotion_record_service import (
    create_emotion_record,
    get_user_emotion_records,
    get_emotion_patterns,
    update_emotion_record,
    delete_emotion_record
)
from app.models.emotion_record import EmotionRecord

@pytest.fixture
def mock_neo4j_session():
    with patch('app.services.emotion_record_service.db.get_session') as mock_get_session:
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        yield mock_session

@pytest.fixture
def sample_emotion_record():
    return EmotionRecord(
        user_id="test_user",
        timestamp=datetime.now(UTC),
        title="Test Thought",
        situation_description="Test Situation",
        emotion="Anxiety",
        underlying_belief="I'm not good enough"
    )

def test_create_emotion_record_success(mock_neo4j_session, sample_emotion_record):
    # Arrange
    mock_result = Mock()
    mock_result.single.return_value = {
        "r": {
            "id": "test_id",
            "user_id": sample_emotion_record.user_id,
            "timestamp": sample_emotion_record.timestamp.isoformat(),
            "title": sample_emotion_record.title,
            "situation_description": sample_emotion_record.situation_description,
            "emotion": sample_emotion_record.emotion,
            "underlying_belief": sample_emotion_record.underlying_belief,
            "created_at": datetime.now(UTC).isoformat(),
            "updated_at": datetime.now(UTC).isoformat()
        }
    }
    mock_neo4j_session.run.return_value = mock_result

    # Act
    result = create_emotion_record(sample_emotion_record)

    # Assert
    assert result is not None
    assert result.id == "test_id"
    assert result.user_id == sample_emotion_record.user_id
    assert result.emotion == sample_emotion_record.emotion
    mock_neo4j_session.run.assert_called_once()

def test_get_user_emotion_records(mock_neo4j_session):
    # Arrange
    mock_results = [
        {
            "r": {
                "id": "test_id_1",
                "user_id": "test_user",
                "timestamp": datetime.now(UTC).isoformat(),
                "emotion": "Anxiety",
                "created_at": datetime.now(UTC).isoformat(),
                "updated_at": datetime.now(UTC).isoformat()
            }
        },
        {
            "r": {
                "id": "test_id_2",
                "user_id": "test_user",
                "timestamp": datetime.now(UTC).isoformat(),
                "emotion": "Sadness",
                "created_at": datetime.now(UTC).isoformat(),
                "updated_at": datetime.now(UTC).isoformat()
            }
        }
    ]
    mock_neo4j_session.run.return_value = mock_results

    # Act
    results = get_user_emotion_records("test_user")

    # Assert
    assert len(results) == 2
    assert results[0].id == "test_id_1"
    assert results[1].id == "test_id_2"

def test_get_emotion_patterns(mock_neo4j_session):
    # Arrange
    mock_results = [
        {"emotion": "Anxiety", "count": 5},
        {"emotion": "Sadness", "count": 3},
        {"emotion": "Anger", "count": 2}
    ]
    mock_neo4j_session.run.return_value = mock_results

    # Act
    patterns = get_emotion_patterns("test_user")

    # Assert
    assert len(patterns) == 3
    assert patterns[0]["emotion"] == "Anxiety"
    assert patterns[0]["count"] == 5

def test_update_emotion_record(mock_neo4j_session):
    # Arrange
    mock_result = Mock()
    mock_result.single.return_value = {
        "r": {
            "id": "test_id",
            "user_id": "test_user",
            "timestamp": datetime.now(UTC).isoformat(),
            "emotion": "Updated Emotion",
            "created_at": datetime.now(UTC).isoformat(),
            "updated_at": datetime.now(UTC).isoformat()
        }
    }
    mock_neo4j_session.run.return_value = mock_result

    # Act
    result = update_emotion_record("test_id", {"emotion": "Updated Emotion"})

    # Assert
    assert result is not None
    assert result.emotion == "Updated Emotion"
    mock_neo4j_session.run.assert_called_once()

def test_delete_emotion_record(mock_neo4j_session):
    # Arrange
    mock_result = Mock()
    mock_result.single.return_value = {"deleted": 1}
    mock_neo4j_session.run.return_value = mock_result

    # Act
    result = delete_emotion_record("test_id")

    # Assert
    assert result is True
    mock_neo4j_session.run.assert_called_once() 