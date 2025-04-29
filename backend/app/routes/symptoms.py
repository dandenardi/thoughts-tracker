from fastapi import APIRouter, HTTPException, Security
from app.db.connection import Neo4jConnection
from app.models.symptom import Symptom
from app.services.symptom_service import add_symptom, get_all_symptoms_from_db
from app.dependencies.auth_dependency import get_current_user
from app.services.symptom_service import get_symptom_time_patterns

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

@router.get("/symptoms-time-patterns")
async def get_symptoms_time_patterns_handler(
    current_user = Security(get_current_user)
):
    """
    Correlates symptoms and day periods using:
    - User -> Thought (already have timestamp)
    - Thought -> Symptom (existent relationship)
    """
    try:
        patterns_data = get_symptom_time_patterns(current_user.uid)

        if not patterns_data:
            return{
                "status": "success",
                "data": [],
                "message": "No thoughts with symptoms found for time pattern analysis"
            }
        
        return {
            "status": "success",
            "data": patterns_data,
            "message": "Symptom time patterns retrieved successfully"
        }

    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing symptom time patterns: {str(e)}"
        )