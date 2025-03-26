from fastapi import APIRouter, HTTPException
from app.db.connection import Neo4jConnection
from app.models.emotions import Emotion
from app.services.emotion_service import add_emotion_to_db, get_all_emotions_from_db
router = APIRouter()

db = Neo4jConnection()

@router.post("/")
async def add_emotion(emotion: Emotion):
    try:
        # Chamando o serviço para adicionar a emoção
        add_emotion_to_db(emotion)
        return {"message": "Emotion added successfully", "emotion": emotion.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/")
def get_all_emotions():
    return get_all_emotions_from_db()

