from fastapi import APIRouter
from app.models.emotion import Emotion
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

def get_emotion_frequency(user_id: str) -> list[dict]:
    query = """
    MATCH (u:User {uid: $user_id})-[:HAS_RECORD]->(t:Thought)
    RETURN t.emotion AS emotion, count(t) AS count
    ORDER BY count DESC
    LIMIT 5
    """
    try:
        with db.get_session() as session:
            result = session.run(query, {"user_id": user_id})
            return [{"emotion": record["emotion"], "count": record["count"]} for record in result]
    except Exception as e:
        print(f"Error fetching emotion frequency: {e}")
        raise e    