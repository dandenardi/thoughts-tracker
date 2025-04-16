from datetime import datetime, timezone
from typing import List, Optional
from app.models.thought_record import ThoughtRecord
from app.db.connection import Neo4jConnection

db = Neo4jConnection()

def create_thought(record: ThoughtRecord) -> ThoughtRecord:
    try:
        query = """
        MATCH (u:User {uid: $user_id})
        CREATE (r:ThoughtRecord {
            id: randomUUID(),
            user_id: $user_id,
            timestamp: $timestamp,
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
            result = session.run(query, {
                "user_id": record.user_id,
                "timestamp": record.timestamp.astimezone(timezone.utc),
                "title": record.title,
                "situation_description": record.situation_description,
                "symptoms": record.symptoms,
                "emotion": record.emotion,
                "underlying_belief": record.underlying_belief
            }).single()

        if result:
            record_data = result["r"]
            timestamp = record_data["timestamp"]

            if hasattr(timestamp, "to_native"):
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
        print(f"Error creating thought record: {e}")
        raise e


def get_user_thoughts(
    user_id: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    emotion: Optional[str] = None,
    symptom: Optional[str] = None
) -> List[ThoughtRecord]:
    try:
        query = """
        MATCH (u:User {uid: $user_id})-[:HAS_RECORD]->(r:ThoughtRecord)
        WHERE 1=1
        """
        params = {"user_id": user_id}

        if start_date:
            query += " AND r.timestamp >= $start_date"
            params["start_date"] = start_date.astimezone(timezone.utc)
        
        if end_date:
            query += " AND r.timestamp <= $end_date"
            params["end_date"] = end_date.astimezone(timezone.utc)
        
        if emotion:
            query += " AND r.emotion = $emotion"
            params["emotion"] = emotion

        if symptom:
            query += " AND $symptom IN r.symptoms"
            params["symptom"] = symptom

        query += " RETURN r ORDER BY r.timestamp DESC"

        with db.get_session() as session:
            results = session.run(query, params)
            raw_data = results.data()

        records = []
        for result in raw_data:
            record_data = result["r"]
            timestamp = record_data["timestamp"]

            if hasattr(timestamp, "to_native"):
                parsed_timestamp = timestamp.to_native()
            else:
                parsed_timestamp = timestamp

            records.append(ThoughtRecord(
                id=record_data["id"],
                user_id=record_data["user_id"],
                timestamp=parsed_timestamp,
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


def update_thought(record_id: str, updates: dict) -> Optional[ThoughtRecord]:
    try:
        updates["updated_at"] = datetime.now(timezone.utc)

        if "timestamp" in updates and isinstance(updates["timestamp"], str):
            updates["timestamp"] = datetime.fromisoformat(updates["timestamp"]).astimezone(timezone.utc)
        elif "timestamp" in updates and isinstance(updates["timestamp"], datetime):
            updates["timestamp"] = updates["timestamp"].astimezone(timezone.utc)

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
            timestamp = record_data["timestamp"]

            if hasattr(timestamp, "to_native"):
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
        return None

    except Exception as e:
        print(f"Error updating thought record: {e}")
        raise e


def delete_thought(record_id: str) -> bool:
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
        print(f"Error deleting thought record: {e}")
        raise e
