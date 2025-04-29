from pydantic import BaseModel, ConfigDict
from typing import ClassVar, Optional

class Emotion(BaseModel):
    id: Optional[str] = None  # Optional because new emotions won't have an ID until saved
    name: str
    description: Optional[str] = None

    # Definindo Config corretamente como ClassVar
    Config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            name=data["name"],
            description=data.get("description")
        )
