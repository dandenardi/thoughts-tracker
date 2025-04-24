from app.models.symptom import Symptom
from app.db.connection import Neo4jConnection

db = Neo4jConnection()

def add_symptom(name: str, description: str = None) -> Symptom:
    """
    Add a new symptom to the database
    """

    query="""
    CREATE (s:Symptom {id: randomUUID(), name: $name, description: $description})
    RETURN s
    """

    with db.get_session() as session:
        result = session.run(query, name=name, description=description).single()
        if result:
            symptom_data = result["s"]
            return Symptom(
                id=symptom_data["id"],
                name=symptom_data["name"],
                description=symptom_data.get("description")
            )
        
        return None
    
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

