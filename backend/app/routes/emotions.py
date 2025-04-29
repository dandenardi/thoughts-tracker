from fastapi import APIRouter, HTTPException, Depends, Security
from typing import List, Optional, Dict, Any
from app.db.connection import Neo4jConnection
from app.models.emotion import Emotion
from app.dependencies.auth_dependency import get_current_user
from app.services.emotion_service import add_emotion, get_all_emotions_from_db, get_emotion_frequency

router = APIRouter()

db = Neo4jConnection()

@router.post("/")
async def add_emotion_endpoint(emotion: Emotion):
    try:
        # Calling the service to add the emotion
        result = add_emotion(emotion.name, emotion.description)
        return {"message": "Emotion added successfully", "emotion": result.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/")
def get_all_emotions():
    emotions = get_all_emotions_from_db()
    return {"emotions": [emotion.model_dump() for emotion in emotions]}


@router.get("/emotions-frequency", response_model=Dict[str, Any])
async def get_emotion_insights_summary_handler(
    current_user = Security(get_current_user)
    ):
    """
    Get the top 5 most frequent emotions for the current user.
    Returns:
        list[dict]: List of emotions with their counts, sorted by frequency
        Example: [{"emotion": "happy", "count": 5}, ...]
    """
    try:
        emotions_data = get_emotion_frequency(current_user.uid)
        if not emotions_data:
            return {
                "status": "success",
                "data": [],
                "message": "No emotion data found for this user"
            }
        return {
            "status": "success",
            "data": emotions_data,
            "message": "Emotion frequency retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))