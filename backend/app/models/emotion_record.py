from datetime import datetime, UTC
from typing import Optional, List
from pydantic import BaseModel

class EmotionRecord(BaseModel):
    id: Optional[str] = None  # Will be set by Neo4j
    user_id: str
    timestamp: datetime
    title: Optional[str] = None
    situation_description: Optional[str] = None
    symptons: Optional[List[str]] = []
    emotion: str
    underlying_belief: Optional[str] = None
    created_at: datetime = datetime.now(UTC)
    updated_at: datetime = datetime.now(UTC) 