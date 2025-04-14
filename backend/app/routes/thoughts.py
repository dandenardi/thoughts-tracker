from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Security
from app.models.thought_record import ThoughtRecord, ThoughtRecordCreate
from app.services.thought_service import (
    create_thought,
    get_user_thoughts,
    get_thought_patterns,
    update_thought_record,
    delete_thought
)
from app.dependencies.auth_dependency import get_current_user

router = APIRouter(
    prefix="/thought-records",
    tags=["thought-records"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ThoughtRecord)
async def create_thought_handler(
    record: ThoughtRecordCreate,
    current_user = Security(get_current_user)
):
    try:
        full_record = ThoughtRecord(
            id="",  # vai ser gerado no banco
            user_id=current_user.uid,
            timestamp=datetime.utcnow(),  # ou None, se for gerado no banco
            title=record.title,
            situation_description=record.situation_description,
            emotion=record.emotion,
            underlying_belief=record.underlying_belief,
            symptoms=record.symptoms,
        )
        return create_thought(full_record)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[ThoughtRecord])
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

@router.put("/{record_id}", response_model=ThoughtRecord)
async def update_thoughts_handler(
    record_id: str,
    updates: dict,
    current_user = Security(get_current_user)
):
    try:
        records = get_user_thoughts(user_id=current_user.uid)
        record_ids = [r.id for r in records]

        if record_id not in record_ids:
            raise HTTPException(status_code=404, detail="Record not found")
            
        return update_thought_record(record_id, updates)
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
