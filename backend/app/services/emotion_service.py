from fastapi import APIRouter
from app.models.emotions import Emotion
from app.db.connection import Neo4jConnection

router = APIRouter()
db = Neo4jConnection()

def add_emotion(name: str, description: str = None) -> Emotion:
    """
    Add a new emotion to the database.
    """
    query = """
    CREATE (e:Emotion {id: randomUUID(), name: $name, description: $description})
    RETURN e
    """
    with db.get_session() as session:
        result = session.run(query, name=name, description=description).single()
        if result:
            emotion_data = result["e"]
            return Emotion(
                id=emotion_data["id"],
                name=emotion_data["name"],
                description=emotion_data.get("description")
            )
        return None

def get_all_emotions_from_db() -> list[Emotion]:
    """
    Get all emotions from the database.
    """
    query = "MATCH (e:Emotion) RETURN e"
    with db.get_session() as session:
        results = session.run(query)
        return [
            Emotion(
                id=record["e"]["id"],
                name=record["e"]["name"],
                description=record["e"].get("description")
            )
            for record in results
        ]
