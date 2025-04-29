from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel

class Thought(BaseModel):
    id: Optional[str] = None  # Will be set by Neo4j
    user_id: str
    timestamp: datetime
    title: Optional[str] = None
    situation_description: Optional[str] = None
    symptoms: Optional[List[str]] = []
    emotion: str
    underlying_belief: Optional[str] = None
    analysis: Optional[Dict] = {}


class ThoughtCreate(BaseModel):
    title: str
    situation_description: str
    emotion: str
    underlying_belief: str
    symptoms: List[str]
