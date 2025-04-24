from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, Security
from app.models.thought import Thought, ThoughtCreate
from app.services.thought_service import (
    create_thought,
    get_user_thoughts,
    get_thought_patterns,
    update_thought,
    delete_thought,
    get_insights_summary
)
from app.dependencies.auth_dependency import get_current_user
from app.services.emotion_service import get_all_emotions_from_db

router = APIRouter(
    tags=["thought-records"],
)

@router.post("/", response_model=Thought)
async def create_thought_handler(
    record: ThoughtCreate,
    current_user = Security(get_current_user)
):
    try:
        
        emotions = get_all_emotions_from_db()

        if record.emotion not in [emotion.name for emotion in emotions]:
            raise HTTPException(status_code=40, detail="Invalid emotion provided")

        full_record = Thought(
            id="",  # vai ser gerado no banco
            user_id=current_user.uid,
            timestamp=datetime.now(timezone.utc),  # ou None, se for gerado no banco
            title=record.title,
            situation_description=record.situation_description,
            emotion=record.emotion,
            underlying_belief=record.underlying_belief,
            symptoms=record.symptoms,
        )
        return create_thought(current_user.uid, full_record)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Thought])
async def get_thoughts_handler(
    start_date: Optional[datetime] = Query(None, description="Start date for filtering records"),
    end_date: Optional[datetime] = Query(None, description="End date for filtering records"),
    emotion: Optional[str] = Query(None, description="Filter by emotion type"),
    symptom: Optional[str] = Query(None, description="Filter by symptom"),
    current_user = Security(get_current_user)
):
    try:
        
        return get_user_thoughts(
            user_id=current_user.uid,
            start_date=start_date,
            end_date=end_date,
            emotion=emotion,
            symptom=symptom
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/patterns", response_model=List[dict])
async def get_patterns_handler(current_user = Security(get_current_user)):
    try:
        return get_thought_patterns(current_user.uid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{record_id}", response_model=Thought)
async def update_thoughts_handler(
    record_id: str,
    record: ThoughtCreate,
    current_user = Security(get_current_user)
):
    try:
        emotions = get_all_emotions_from_db()

        # Validação de emoção
        if record.emotion not in [emotion.name for emotion in emotions]:
            raise HTTPException(status_code=400, detail="Invalid emotion provided")

        # Verificação se o pensamento pertence ao usuário
        records = get_user_thoughts(user_id=current_user.uid)
        record_ids = [r.id for r in records]

        if record_id not in record_ids:
            raise HTTPException(status_code=404, detail="Record not found")
        
        # Montagem do dicionário de atualizações
        updates = {
            "user_id": current_user.uid,
            "timestamp": datetime.now(timezone.utc),
            "title": record.title,
            "situation_description": record.situation_description,
            "emotion": record.emotion,  # Emoção validada
            "underlying_belief": record.underlying_belief,
            "symptoms": record.symptoms,
        }
        
        # Chamada da função de atualização
        updated_record = update_thought(record_id, updates)
        if not updated_record:
            raise HTTPException(status_code=404, detail="Record not found")
        
        return updated_record
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{record_id}")
async def delete_thoughts_handler(
    record_id: str,
    current_user = Security(get_current_user)
):
    try:
        records = get_user_thoughts(user_id=current_user.uid)
        record_ids = [r.id for r in records]

        if record_id not in record_ids:
            raise HTTPException(status_code=404, detail="Record not found")

        success = delete_thought(record_id)
        if not success:
            raise HTTPException(status_code=404, detail="Record not found")
        return {"message": "Record deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/insights-summary", response_model=Dict[str, Any])
async def get_insights_summary_handler(
    current_user = Security(get_current_user)
    ):
    try:
        insights = get_insights_summary(current_user.uid)
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))