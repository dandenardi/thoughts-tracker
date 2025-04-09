import pytest
from datetime import datetime, UTC
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.main import app
from app.models.users import User
from app.models.emotion_record import EmotionRecord

client = TestClient(app)

@pytest.fixture
def mock_current_user():
    return User(
        uid="test_user",
        email="test@example.com",
        name="Test User"
    )

@pytest.fixture
def mock_emotion_record():
    return EmotionRecord(
        user_id="test_user",
        timestamp=datetime.now(UTC),
        title="Test Thought",
        situation_description="Test Situation",
        emotion="Anxiety",
        underlying_belief="I'm not good enough"
    )

def test_create_record_success(mock_current_user, mock_emotion_record):
    # Arrange
    with patch('app.routes.emotion_records.verify_token', return_value=mock_current_user), \
         patch('app.routes.emotion_records.create_emotion_record', return_value=mock_emotion_record):
        
        # Convert datetime to ISO format for JSON serialization
        record_dict = mock_emotion_record.model_dump()
        record_dict['timestamp'] = record_dict['timestamp'].isoformat()
        record_dict['created_at'] = record_dict['created_at'].isoformat()
        record_dict['updated_at'] = record_dict['updated_at'].isoformat()
        
        # Act
        response = client.post(
            "/emotion-records/",
            json=record_dict,
            headers={"Authorization": "Bearer test_token"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["emotion"] == mock_emotion_record.emotion
        assert data["title"] == mock_emotion_record.title

def test_get_records_success(mock_current_user):
    # Arrange
    mock_records = [
        EmotionRecord(
            id="test_id_1",
            user_id="test_user",
            timestamp=datetime.now(UTC),
            emotion="Anxiety"
        ),
        EmotionRecord(
            id="test_id_2",
            user_id="test_user",
            timestamp=datetime.now(UTC),
            emotion="Sadness"
        )
    ]
    
    with patch('app.routes.emotion_records.verify_token', return_value=mock_current_user), \
         patch('app.routes.emotion_records.get_user_emotion_records', return_value=mock_records):
        
        # Act
        response = client.get(
            "/emotion-records/",
            headers={"Authorization": "Bearer test_token"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["emotion"] == "Anxiety"
        assert data[1]["emotion"] == "Sadness"

def test_get_patterns_success(mock_current_user):
    # Arrange
    mock_patterns = [
        {"emotion": "Anxiety", "count": 5},
        {"emotion": "Sadness", "count": 3}
    ]
    
    with patch('app.routes.emotion_records.verify_token', return_value=mock_current_user), \
         patch('app.routes.emotion_records.get_emotion_patterns', return_value=mock_patterns):
        
        # Act
        response = client.get(
            "/emotion-records/patterns",
            headers={"Authorization": "Bearer test_token"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["emotion"] == "Anxiety"
        assert data[0]["count"] == 5

def test_update_record_success(mock_current_user):
    # Arrange
    mock_record = EmotionRecord(
        id="test_id",
        user_id="test_user",
        timestamp=datetime.now(UTC),
        emotion="Updated Emotion"
    )
    
    with patch('app.routes.emotion_records.verify_token', return_value=mock_current_user), \
         patch('app.routes.emotion_records.get_user_emotion_records', return_value=[mock_record]), \
         patch('app.routes.emotion_records.update_emotion_record', return_value=mock_record):
        
        # Act
        response = client.put(
            "/emotion-records/test_id",
            json={"emotion": "Updated Emotion"},
            headers={"Authorization": "Bearer test_token"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["emotion"] == "Updated Emotion"

def test_delete_record_success(mock_current_user):
    # Arrange
    mock_record = EmotionRecord(
        id="test_id",
        user_id="test_user",
        timestamp=datetime.now(UTC),
        emotion="Test Emotion"
    )
    
    with patch('app.routes.emotion_records.verify_token', return_value=mock_current_user), \
         patch('app.routes.emotion_records.get_user_emotion_records', return_value=[mock_record]), \
         patch('app.routes.emotion_records.delete_emotion_record', return_value=True):
        
        # Act
        response = client.delete(
            "/emotion-records/test_id",
            headers={"Authorization": "Bearer test_token"}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Record deleted successfully"

def test_delete_record_not_found(mock_current_user):
    # Arrange
    with patch('app.routes.emotion_records.verify_token', return_value=mock_current_user), \
         patch('app.routes.emotion_records.get_user_emotion_records', return_value=[]):
        
        # Act
        response = client.delete(
            "/emotion-records/non_existent_id",
            headers={"Authorization": "Bearer test_token"}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Record not found" 