from pydantic import BaseModel

class Symptom(BaseModel):
    id: str
    name: str
    description: str | None = None
    intensity: str | None = None