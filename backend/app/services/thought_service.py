from datetime import datetime, timezone
from typing import List, Optional
from app.models.thought import Thought, ThoughtCreate
from app.db.connection import Neo4jConnection
from neo4j.time import DateTime

db = Neo4jConnection()

def create_thought(user_id: str, data: ThoughtCreate) -> Thought:
    try:
        # Normaliza os sintomas (remove duplicados e espaços em branco)
        normalized_symptoms = []
        if data.symptoms:
            normalized_symptoms = list({symptom.lower().strip() for symptom in data.symptoms if symptom.strip()})
        
        # Prepara o timestamp
        input_timestamp = data.timestamp.astimezone(timezone.utc) if data.timestamp else datetime.now(timezone.utc)
        neo4j_timestamp = input_timestamp.isoformat(timespec='milliseconds')

        # Query base sem sintomas
        query = """
        MATCH (u:User {uid: $user_id})
        CREATE (t:Thought {
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
        CREATE (u)-[:HAS_RECORD]->(t)
        """
        
        # Adiciona tratamento de sintomas se existirem
        if normalized_symptoms:
            query += """
            WITH t
            UNWIND $symptoms AS symptom_name
            OPTIONAL MATCH (s:Symptom {name: symptom_name})
            WITH t, collect(s) AS symptom_nodes
            WHERE size(symptom_nodes) = size($symptoms)
            FOREACH (s IN symptom_nodes | CREATE (t)-[:HAS_SYMPTOM]->(s))
            """
        
        # Finaliza a query com RETURN
        query += """
        RETURN properties(t) as thought_props,
               t.timestamp as db_timestamp
        """
        
        # Parâmetros para a query
        params = {
            "user_id": user_id,
            "timestamp": neo4j_timestamp,
            "title": data.title,
            "situation_description": data.situation_description,
            "emotion": data.emotion,
            "underlying_belief": data.underlying_belief
        }
        
        # Adiciona sintomas aos parâmetros se existirem
        if normalized_symptoms:
            params["symptoms"] = normalized_symptoms

        with db.get_session() as session:
            result = session.run(query, params).single()

            if not result:
                raise ValueError("Erro ao criar registro de pensamento")

            thought_props = dict(result["thought_props"])
            db_timestamp = result["db_timestamp"]
            
            return Thought(
                id=thought_props["id"],
                user_id=user_id,
                timestamp=db_timestamp.to_native(),
                title=thought_props["title"],
                situation_description=thought_props["situation_description"],
                emotion=thought_props["emotion"],
                underlying_belief=thought_props["underlying_belief"],
                symptoms=normalized_symptoms,
                analysis={}
            )


    except Exception as e:
        print(f"Error creating thought: {e}")
        raise e

def get_user_thoughts(
    user_id: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    emotion: Optional[str] = None,
    symptom: Optional[str] = None
) -> List[Thought]:
    try:
        query = """
        MATCH (u:User {uid: $user_id})-[:HAS_RECORD]->(r:Thought)
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

        thoughts = []
        for result in raw_data:
            record_data = result["r"]
            timestamp = record_data["timestamp"]

            if hasattr(timestamp, "to_native"):
                parsed_timestamp = timestamp.to_native()
            else:
                parsed_timestamp = timestamp

            thoughts.append(Thought(
                id=record_data["id"],
                user_id=record_data["user_id"],
                timestamp=parsed_timestamp,
                title=record_data.get("title"),
                situation_description=record_data.get("situation_description"),
                symptoms=record_data.get("symptoms", []),
                emotion=record_data["emotion"],
                underlying_belief=record_data.get("underlying_belief"),
            ))
        
        return thoughts

    except Exception as e:
        print(f"Error getting user thought records: {e}")
        raise e


def get_thought_patterns(user_id: str) -> List[dict]:
    try:
        query = """
        MATCH (u:User {uid: $user_id})-[:HAS_RECORD]->(r:Thought)
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


def update_thought(record_id: str, updates: dict) -> Optional[Thought]:
    try:
        updates["updated_at"] = datetime.now(timezone.utc)

        if "timestamp" in updates and isinstance(updates["timestamp"], str):
            updates["timestamp"] = datetime.fromisoformat(updates["timestamp"]).astimezone(timezone.utc)
        elif "timestamp" in updates and isinstance(updates["timestamp"], datetime):
            updates["timestamp"] = updates["timestamp"].astimezone(timezone.utc)

        if "symptoms" in updates and not isinstance(updates["symptoms"], list):
            updates["symptoms"] = [updates["symptoms"]]

        query = """
        MATCH (r:Thought {id: $record_id})
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

            return Thought(
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
        MATCH (r:Thought {id: $record_id})
        DETACH DELETE r
        RETURN count(r) as deleted
        """

        with db.get_session() as session:
            result = session.run(query, record_id=record_id).single()

        return result["deleted"] > 0

    except Exception as e:
        print(f"Error deleting thought record: {e}")
        raise e

def get_top_emotions(session, user_id):
    query = """
    Match (t:Thought {user_id: $user_id})
    RETURN t.emotion AS emotion, count(*) AS count
    ORDER BY count DESC
    LIMIT 3
    """

    result = session.run(query, {"user_id": user_id})
    return [record["emotion"] for record in result]

def get_common_hours(session, user_id):
    query = """
    MATCH (t:Thought {user_id: $user_id})
    WITH datetime(t.timestamp).hour AS hour
    RETURN hour, count(*) AS count
    ORDER BY count DESC
    LIMIT 3
    """

    result = session.run(query, {"user_id": user_id})
    return [f"{record['hour']}h - {int(record['hour'])+2}h" for record in result]

def get_most_common_symptom(session, user_id: str) -> str:
    query = """
    MATCH (t:Thought {user_id: $user_id})-[:HAS_SYMPTOM]->(s:Symptom)
    RETURN s.name AS symptom, count(*) AS count
    ORDER BY count DESC
    LIMIT 1
    """
    
    result = session.run(query, {"user_id": user_id}).single()
    return result["symptom"] if result else "N/A"

def get_frequent_keywords(session, user_id):

    STOPWORDS_EN = ["because", "then", "after", "also", "with", "from", "that", "have", "this"]

    query= """
        MATCH (t:Thought {user_id: $user_id})
        WITH apoc.text.clean(t.title + ' ' + t.situation_description) AS text
        WITH apoc.text.split(text, "\\\W+") AS words
        UNWIND words AS word
        WITH toLower(word) AS word
        WHERE size(word) > 3 AND NOT word IN $stopwords
        RETURN word, count(*) AS count
        ORDER BY count DESC
        LIMIT 5
    """

    result = session.run(query, {
        "user_id": user_id,
        "stopwords": STOPWORDS_EN
    })
    return [record["word"] for record in result]

def count_active_days(session, user_id: str) -> int:
    query = """
    MATCH (t:Thought {user_id: $user_id})
    RETURN count(DISTINCT date(datetime(t.timestamp))) AS days
    """
    
    result = session.run(query, {"user_id": user_id})
    return result.single()["days"]

def count_user_thoughts(session, user_id: str) -> int:
    query = """
    MATCH (t:Thought {user_id: $user_id})
    RETURN count(t) AS total
    """
    
    result = session.run(query, {"user_id": user_id})
    return result.single()["total"]

def get_insights_summary(user_id: str) -> dict:
    with db.get_session() as session:
        return {
            "total_thoughts": count_user_thoughts(session, user_id),
            "top_emotions": get_top_emotions(session, user_id),
            "most_common_symptom": get_most_common_symptom(session, user_id),
            "common_time_ranges": get_common_hours(session, user_id),
            "frequent_keywords": get_frequent_keywords(session, user_id),
            "active_days": count_active_days(session, user_id)  
        }