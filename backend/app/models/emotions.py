from pydantic import BaseModel, ConfigDict
from typing import ClassVar

class Emotion(BaseModel):
    name: str  # Define o campo 'name' como uma string obrigatória.

    # Definindo Config corretamente como ClassVar
    Config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    def to_dict(self):
        return {"name": self.name}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(name=data["name"])
