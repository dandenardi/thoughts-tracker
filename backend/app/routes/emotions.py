from fastapi import APIRouter, HTTPException
from app.db.connection import Neo4jConnection
from app.models.emotions import Emotion
from app.services.emotion_service import add_emotion, get_all_emotions_from_db

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

