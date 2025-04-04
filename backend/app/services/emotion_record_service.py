from datetime import datetime
from typing import List, Optional
from app.models.emotion_record import EmotionRecord
from app.db.connection import Neo4jConnection

db = Neo4jConnection()

def create_emotion_record(record: EmotionRecord) -> EmotionRecord:
    """
    Create a new emotion record in the database.
    """
    try:
        query = """
        MATCH (u:User {uid: $user_id})
        CREATE (r:EmotionRecord {
            id: randomUUID(),
            user_id: $user_id,
            timestamp: datetime($timestamp),
            title: $title,
            situation_description: $situation_description,
            emotion: $emotion,
            underlying_belief: $underlying_belief,
            created_at: datetime(),
            updated_at: datetime()
        })
        CREATE (u)-[:HAS_RECORD]->(r)
        RETURN r
        """

        with db.get_session() as session:
            result = session.run(
                query,
                user_id=record.user_id,
                timestamp=record.timestamp.isoformat(),
                title=record.title,
                situation_description=record.situation_description,
                emotion=record.emotion,
                underlying_belief=record.underlying_belief
            ).single()

        if result:
            record_data = result["r"]
            return EmotionRecord(
                id=record_data["id"],
                user_id=record_data["user_id"],
                timestamp=datetime.fromisoformat(record_data["timestamp"]),
                title=record_data.get("title"),
                situation_description=record_data.get("situation_description"),
                emotion=record_data["emotion"],
                underlying_belief=record_data.get("underlying_belief"),
                created_at=datetime.fromisoformat(record_data["created_at"]),
                updated_at=datetime.fromisoformat(record_data["updated_at"])
            )
        return None

    except Exception as e:
        print(f"Error creating emotion record: {e}")
        raise e

def get_user_emotion_records(
    user_id: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    emotion: Optional[str] = None
) -> List[EmotionRecord]:
    """
    Get emotion records for a user with optional filtering.
    """
    try:
        query = """
        MATCH (u:User {uid: $user_id})-[:HAS_RECORD]->(r:EmotionRecord)
        WHERE 1=1
        """
        params = {"user_id": user_id}

        if start_date:
            query += " AND r.timestamp >= datetime($start_date)"
            params["start_date"] = start_date.isoformat()
        
        if end_date:
            query += " AND r.timestamp <= datetime($end_date)"
            params["end_date"] = end_date.isoformat()
        
        if emotion:
            query += " AND r.emotion = $emotion"
            params["emotion"] = emotion

        query += " RETURN r ORDER BY r.timestamp DESC"

        with db.get_session() as session:
            results = session.run(query, params)

        records = []
        for result in results:
            record_data = result["r"]
            records.append(EmotionRecord(
                id=record_data["id"],
                user_id=record_data["user_id"],
                timestamp=datetime.fromisoformat(record_data["timestamp"]),
                title=record_data.get("title"),
                situation_description=record_data.get("situation_description"),
                emotion=record_data["emotion"],
                underlying_belief=record_data.get("underlying_belief"),
                created_at=datetime.fromisoformat(record_data["created_at"]),
                updated_at=datetime.fromisoformat(record_data["updated_at"])
            ))
        return records

    except Exception as e:
        print(f"Error getting user emotion records: {e}")
        raise e

def get_emotion_patterns(user_id: str) -> List[dict]:
    """
    Analyze emotion patterns for a user, including:
    - Most common emotions
    - Time patterns (e.g., emotions by time of day)
    - Common underlying beliefs
    """
    try:
        query = """
        MATCH (u:User {uid: $user_id})-[:HAS_RECORD]->(r:EmotionRecord)
        WITH r.emotion as emotion, count(*) as count
        ORDER BY count DESC
        RETURN emotion, count
        LIMIT 5
        """

        with db.get_session() as session:
            results = session.run(query, user_id=user_id)

        return [{"emotion": result["emotion"], "count": result["count"]} 
                for result in results]

    except Exception as e:
        print(f"Error getting emotion patterns: {e}")
        raise e

def update_emotion_record(record_id: str, updates: dict) -> Optional[EmotionRecord]:
    """
    Update an existing emotion record.
    """
    try:
        query = """
        MATCH (r:EmotionRecord {id: $record_id})
        SET r += $updates,
            r.updated_at = datetime()
        RETURN r
        """

        with db.get_session() as session:
            result = session.run(query, record_id=record_id, updates=updates).single()

        if result:
            record_data = result["r"]
            return EmotionRecord(
                id=record_data["id"],
                user_id=record_data["user_id"],
                timestamp=datetime.fromisoformat(record_data["timestamp"]),
                title=record_data.get("title"),
                situation_description=record_data.get("situation_description"),
                emotion=record_data["emotion"],
                underlying_belief=record_data.get("underlying_belief"),
                created_at=datetime.fromisoformat(record_data["created_at"]),
                updated_at=datetime.fromisoformat(record_data["updated_at"])
            )
        return None

    except Exception as e:
        print(f"Error updating emotion record: {e}")
        raise e

def delete_emotion_record(record_id: str) -> bool:
    """
    Delete an emotion record.
    """
    try:
        query = """
        MATCH (r:EmotionRecord {id: $record_id})
        DETACH DELETE r
        RETURN count(r) as deleted
        """

        with db.get_session() as session:
            result = session.run(query, record_id=record_id).single()

        return result["deleted"] > 0

    except Exception as e:
        print(f"Error deleting emotion record: {e}")
        raise e 