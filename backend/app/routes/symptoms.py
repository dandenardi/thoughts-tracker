from fastapi import APIRouter, HTTPException
from app.db.connection import Neo4jConnection
from app.models.symptom import Symptom
from app.services.symptom_service import add_symptom, get_all_symptoms_from_db

router = APIRouter()

@router.post("/")
async def add_symptom_endpoint(symptom: Symptom):
    try:

        result = add_symptom(symptom.name, symptom.description)
        return {"message": "Symptom added successfully", "symptom": result.model_dump()}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@router.get("/")
def get_all_symptoms():
    symptoms=get_all_symptoms_from_db()
    return {"symptoms": [symptom.model_dump() for symptom in symptoms]}