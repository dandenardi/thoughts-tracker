from datetime import datetime
from typing import List, Optional
from app.models.thought_record import ThoughtRecord
from app.db.connection import Neo4jConnection

db = Neo4jConnection()

def create_thought(record: ThoughtRecord) -> ThoughtRecord:
    """
    Create a new emotion record in the database.
    """
    try:
        query = """
        MATCH (u:User {uid: $user_id})
        CREATE (r:ThoughtRecord {
            id: randomUUID(),
            user_id: $user_id,
            timestamp: datetime($timestamp),
            title: $title,
            situation_description: $situation_description,
            symptoms: $symptoms,
            emotion: $emotion,
            underlying_belief: $underlying_belief,
            created_at: datetime(),
            updated_at: datetime()
            
        })
        CREATE (u)-[:HAS_RECORD]->(r)
        RETURN r
        """

        with db.get_session() as session:
            result = session.run(query,{

                "user_id":record.user_id,
                "timestamp":record.timestamp.isoformat(),
                "title":record.title,
                "situation_description":record.situation_description,
                "symptoms": record.symptoms,
                "emotion":record.emotion,
                "underlying_belief":record.underlying_belief
            }).single()

        if result:
            record_data = result["r"]
            
            timestamp = record_data["timestamp"]

            if isinstance(timestamp, str):
                parsed_timestamp = datetime.fromisoformat(timestamp)
            elif hasattr(timestamp, "to_native"):
                parsed_timestamp = timestamp.to_native()
            else:
                parsed_timestamp = timestamp
            
            return ThoughtRecord(
                id=record_data["id"],
                user_id=record_data["user_id"],
                timestamp=parsed_timestamp,
                title=record_data.get("title"),
                situation_description=record_data.get("situation_description"),
                symptoms=record_data.get("symptoms", []),
                emotion=record_data["emotion"],
                underlying_belief=record_data.get("underlying_belief"),
            )

    except Exception as e:
        print(f"Error creating emotion record: {e}")
        raise e

def get_user_thoughts(
    user_id: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    emotion: Optional[str] = None,
    symptom: Optional[str] = None
) -> List[ThoughtRecord]:
    """
    Get thought records for a user with optional filtering.
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

        if symptom:
            query += " AND symptom IN r.symptoms"
            params["symptom"] = symptom

        query += " RETURN r ORDER BY r.timestamp DESC"

        with db.get_session() as session:
            results = session.run(query, params)

        records = []
        for result in results:
            record_data = result["r"]
            records.append(ThoughtRecord(
                id=record_data["id"],
                user_id=record_data["user_id"],
                timestamp=datetime.fromisoformat(record_data["timestamp"]),
                title=record_data.get("title"),
                situation_description=record_data.get("situation_description"),
                symptoms=record_data.get("symptoms", []),
                emotion=record_data["emotion"],
                underlying_belief=record_data.get("underlying_belief"),
                
            ))
        return records

    except Exception as e:
        print(f"Error getting user thought records: {e}")
        raise e
    

def get_thought_patterns(user_id: str) -> List[dict]:
    """
    Analyze emotion patterns for a user:
    - Most common emotions (top 5)
    """
    try:
        query = """
        MATCH (u:User {uid: $user_id})-[:HAS_RECORD]->(r:ThoughtRecord)
        WITH r.emotion AS emotion, count(*) AS count
        ORDER BY count DESC
        RETURN emotion, count
        LIMIT 5
        """

        with db.get_session() as session:
            results = session.run(query, user_id=user_id)

        return [{"emotion": result["emotion"], "count": result["count"]}
                for result in results]

    except Exception as e:
        print(f"Error getting thought patterns: {e}")
        raise e


def update_thought_record(record_id: str, updates: dict) -> Optional[ThoughtRecord]:
    """
    Update an existing thought record.
    """
    try:
        # Atualização de timestamp automática
        updates["updated_at"] = datetime.now(datetime.UTC).isoformat()

        # Caso esteja passando symptoms via JSON, precisamos garantir que seja uma lista
        if "symptoms" in updates and not isinstance(updates["symptoms"], list):
            updates["symptoms"] = [updates["symptoms"]]

        query = """
        MATCH (r:ThoughtRecord {id: $record_id})
        SET r += $updates
        RETURN r
        """

        with db.get_session() as session:
            result = session.run(query, record_id=record_id, updates=updates).single()

        if result:
            record_data = result["r"]
            return ThoughtRecord(
                id=record_data["id"],
                user_id=record_data["user_id"],
                timestamp=datetime.fromisoformat(record_data["timestamp"]),
                title=record_data.get("title"),
                situation_description=record_data.get("situation_description"),
                symptoms=record_data.get("symptoms", []),
                emotion=record_data["emotion"],
                underlying_belief=record_data.get("underlying_belief"),
            )
        return None

    except Exception as e:
        print(f"Error updating thought record: {e}")
        raise e



def delete_thought(record_id: str) -> bool:
    """
    Delete a thought record.
    """
    try:
        query = """
        MATCH (r:ThoughtRecord {id: $record_id})
        DETACH DELETE r
        RETURN count(r) as deleted
        """

        with db.get_session() as session:
            result = session.run(query, record_id=record_id).single()

        return result["deleted"] > 0

    except Exception as e:
        print(f"Error deleting emotion record: {e}")
        raise e 