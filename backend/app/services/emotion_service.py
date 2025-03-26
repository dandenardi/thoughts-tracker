from fastapi import APIRouter
from app.models.emotions import Emotion
from app.db.connection import Neo4jConnection  # Supondo que a conexão com Neo4j esteja definida aqui

router = APIRouter()

db = Neo4jConnection()

# Definir um endpoint para adicionar uma nova emoção
def add_emotion_to_db(emotion: Emotion):
    query = "CREATE (e:Emotion {name: $name})"
    db.get_session().run(query, name=emotion.name)

def get_all_emotions_from_db():
    query = "MATCH (e:Emotion) RETURN e.name AS name"
    with db.get_session() as session:
        result = session.run(query)
        # Acesse 'name', pois é isso que você renomeou na consulta Cypher.
        emotions = [record["name"] for record in result]
    return {"emotions": emotions}