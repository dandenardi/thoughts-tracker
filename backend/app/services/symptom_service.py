from typing import List, Dict
from app.models.symptom import Symptom
from app.db.connection import Neo4jConnection

db = Neo4jConnection()

def normalize_symptom_name(name: str) -> str:
    return name.strip().lower()

def add_symptom(name: str, description: str = None) -> Symptom:
    """
    Add a new symptom to the database
    """
    normalized_name = normalize_symptom_name(name)

    
    with db.get_session() as session:

        result = session.run("""
                             MATCH (s:Symptom {name: $name})
                             RETURN s

                             """, {"name":normalized_name}).single()
        if result:
            node = result["s"]
            return Symptom(name=node["name"], description=node["description"])

        result = session.run(
            """
                CREATE (s:Symptom {
                name: $name,
                description: $description
                })
                RETURN s
            """, {"name": normalized_name, "description": description}).single()
        node = result["s"]
        
        return Symptom(name=node["name"], description=node["description"])
    
def get_all_symptoms_from_db() -> list[Symptom]:
    """
    Get all symptoms from the database.
    """
    query = "MATCH (s:Symptom) RETURN s"
    
    try:
        with db.get_session() as session:
            results = session.run(query)
            
            symptoms = []
            for record in results:
                print("Processing record:", record)  # Imprime o record completo
                
                # Acessar o nó 's'
                node = record.get("s")
                if node:
                    print("Node:", node)
                    
                    # Obter propriedades do nó
                    symptom_id = node.element_id
                    symptom_name = node.get("name")
                    symptom_description = node.get("description", None)
                    
                    # Exibir as propriedades para depuração
                    print(f"Parsed Symptom - ID: {symptom_id}, Name: {symptom_name}, Description: {symptom_description}")
                    
                    # Verificar se o id e nome são válidos
                    if symptom_id and symptom_name:
                        print("Creating Symptom object...")
                        symptom = Symptom(id=symptom_id, name=symptom_name, description=symptom_description)
                        print(f"Symptom created: {symptom}")
                        symptoms.append(symptom)
                    else:
                        print(f"Skipping record due to invalid data - ID or Name missing")
                else:
                    print("No node 's' found in record")
            
            print(f"Symptoms list populated with {len(symptoms)} symptoms")
            return symptoms
    
    except Exception as e:
        print(f"Error occurred while fetching symptoms: {e}")
        raise  # Re-levanta a exceção após logar

def get_symptom_time_patterns(user_id: str) -> List[Dict]:
    """
    Correlates symptoms with hour ranges with proper timestamp handling.
    Returns: List of dictionaries with time_range, symptom, and count
    """
    query = """
    MATCH (u:User {uid: $user_id})-[:HAS_RECORD]->(t:Thought)-[:HAS_SYMPTOM]->(s:Symptom)
    WHERE t.timestamp IS NOT NULL
    WITH 
        datetime(t.timestamp) AS timestamp,
        s.name AS symptom
    WITH
        symptom,
        CASE
            WHEN timestamp.hour >= 5 AND timestamp.hour < 12 THEN 'Morning'
            WHEN timestamp.hour >= 12 AND timestamp.hour < 18 THEN 'Afternoon'
            WHEN timestamp.hour < 5 OR timestamp.hour >= 23 THEN 'Dawn'
            ELSE 'Night'
        END AS time_range
    RETURN 
        time_range,
        symptom,
        count(*) AS count
    ORDER BY time_range, count DESC
    """
    
    try:
        with db.get_session() as session:
            result = session.run(query, {"user_id": user_id})
            patterns = []
            for record in result:
                patterns.append({
                    "time_range": record["time_range"],
                    "symptom": record["symptom"],
                    "count": record["count"]
                })
            return patterns
    except Exception as e:
        print(f"Error fetching symptom time patterns: {e}")
        raise e