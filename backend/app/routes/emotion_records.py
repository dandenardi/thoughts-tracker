from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.emotion_record import EmotionRecord
from app.services.emotion_record_service import (
    create_emotion_record,
    get_user_emotion_records,
    get_emotion_patterns,
    update_emotion_record,
    delete_emotion_record
)
from app.routes.auth import verify_token, oauth2_scheme
from app.models.users import User

router = APIRouter(
    prefix="/emotion-records",
    tags=["emotion-records"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=EmotionRecord)
async def create_record(
    record: EmotionRecord,
    token: str = Depends(oauth2_scheme)
):
    """
    Create a new emotion record.
    """
    try:
        # Get current user from token
        current_user = verify_token(token)
        # Ensure the record is associated with the current user
        record.user_id = current_user.uid
        return create_emotion_record(record)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[EmotionRecord])
async def get_records(
    start_date: Optional[datetime] = Query(None, description="Start date for filtering records"),
    end_date: Optional[datetime] = Query(None, description="End date for filtering records"),
    emotion: Optional[str] = Query(None, description="Filter by emotion type"),
    token: str = Depends(oauth2_scheme)
):
    """
    Get emotion records for the current user with optional filtering.
    """
    try:
        current_user = verify_token(token)
        return get_user_emotion_records(
            user_id=current_user.uid,
            start_date=start_date,
            end_date=end_date,
            emotion=emotion
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/patterns", response_model=List[dict])
async def get_patterns(
    token: str = Depends(oauth2_scheme)
):
    """
    Get emotion patterns and statistics for the current user.
    """
    try:
        current_user = verify_token(token)
        return get_emotion_patterns(current_user.uid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{record_id}", response_model=EmotionRecord)
async def update_record(
    record_id: str,
    updates: dict,
    token: str = Depends(oauth2_scheme)
):
    """
    Update an existing emotion record.
    """
    try:
        current_user = verify_token(token)
        # First check if the record belongs to the user
        records = get_user_emotion_records(current_user.uid)
        record_ids = [r.id for r in records]
        
        if record_id not in record_ids:
            raise HTTPException(status_code=404, detail="Record not found")
            
        return update_emotion_record(record_id, updates)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{record_id}")
async def delete_record(
    record_id: str,
    token: str = Depends(oauth2_scheme)
):
    """
    Delete an emotion record.
    """
    try:
        current_user = verify_token(token)
        # First check if the record belongs to the user
        records = get_user_emotion_records(current_user.uid)
        record_ids = [r.id for r in records]
        
        if record_id not in record_ids:
            raise HTTPException(status_code=404, detail="Record not found")
            
        success = delete_emotion_record(record_id)
        if not success:
            raise HTTPException(status_code=404, detail="Record not found")
        return {"message": "Record deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 