import pytest
from datetime import datetime, UTC
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from backend.app.models.user import User
from backend.app.models.thought import ThoughtRecord, ThoughtRecordCreate

client = TestClient(app)

@pytest.fixture
def mock_current_user():
    return User(
        uid="test_user",
        email="test@example.com",
        name="Test User"
    )

def build_mock_thought_record(id: str = "mock_id") -> ThoughtRecord:
    return ThoughtRecord(
        id=id,
        user_id="test_user",
        timestamp=datetime.now(UTC),
        title="Example Thought",
        situation_description="An example situation",
        emotion="Anxiety",
        underlying_belief="I'm not safe",
        symptoms=["sweaty palms", "racing heart"]
    )

def build_mock_thought_record_create() -> ThoughtRecordCreate:
    return ThoughtRecordCreate(
        user_id="test_user",
        title="Example Thought",
        situation_description="An example situation",
        emotion="Anxiety",
        underlying_belief="I'm not safe",
        symptoms=["sweaty palms", "racing heart"]
    )

def test_create_thought_handler_success(mock_current_user):
    record_create = build_mock_thought_record_create()
    record_response = build_mock_thought_record()

    with patch('app.routes.thoughts.verify_token', return_value=mock_current_user), \
         patch('app.services.thought_service.create_thought', return_value=record_response):

        record_dict = record_create.model_dump()

        response = client.post(
            "/thought-records/",
            json=record_dict,
            headers={"Authorization": "Bearer test_token"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["emotion"] == record_response.emotion
        assert data["title"] == record_response.title

def test_get_thoughts_handler_success(mock_current_user):
    mock_records = [
        build_mock_thought_record(id="1"),
        build_mock_thought_record(id="2")
    ]

    with patch('app.routes.thoughts.verify_token', return_value=mock_current_user), \
         patch('app.services.thought_service.get_user_thoughts', return_value=mock_records):

        response = client.get(
            "/thought-records/",
            headers={"Authorization": "Bearer test_token"}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["emotion"] == "Anxiety"

def test_get_patterns_handler_success(mock_current_user):
    mock_patterns = [
        {"emotion": "Fear", "count": 4},
        {"emotion": "Anger", "count": 2}
    ]

    with patch('app.routes.thoughts.verify_token', return_value=mock_current_user), \
         patch('app.services.thought_service.get_thought_patterns', return_value=mock_patterns):

        response = client.get(
            "/thought-records/patterns",
            headers={"Authorization": "Bearer test_token"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data[0]["emotion"] == "Fear"
        assert data[0]["count"] == 4

def test_update_thoughts_handler_success(mock_current_user):
    original_record = build_mock_thought_record(id="thought_123")
    updated_record = build_mock_thought_record(id="thought_123")
    updated_record.emotion = "Joy"
    updated_record.title = "Updated Title"

    with patch('app.routes.thoughts.verify_token', return_value=mock_current_user), \
         patch('app.services.thought_service.get_user_thoughts', return_value=[original_record]), \
         patch('app.services.thought_service.update_thought_record', return_value=updated_record):

        response = client.put(
            "/thought-records/thought_123",
            json={"emotion": "Joy", "title": "Updated Title"},
            headers={"Authorization": "Bearer test_token"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["emotion"] == "Joy"
        assert data["title"] == "Updated Title"

def test_delete_thoughts_handler_success(mock_current_user):
    mock_record = build_mock_thought_record(id="thought_123")

    with patch('app.routes.thoughts.verify_token', return_value=mock_current_user), \
         patch('app.services.thought_service.get_user_thoughts', return_value=[mock_record]), \
         patch('app.services.thought_service.delete_thought', return_value=True):

        response = client.delete(
            "/thought-records/thought_123",
            headers={"Authorization": "Bearer test_token"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Record deleted successfully"

def test_delete_thoughts_handler_not_found(mock_current_user):
    with patch('app.routes.thoughts.verify_token', return_value=mock_current_user), \
         patch('app.services.thought_service.get_user_thoughts', return_value=[]):

        response = client.delete(
            "/thought-records/nonexistent",
            headers={"Authorization": "Bearer test_token"}
        )

        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Record not found"
