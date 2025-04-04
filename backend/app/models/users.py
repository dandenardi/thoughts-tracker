from pydantic import BaseModel

class User(BaseModel):
    uid: str
    email: str
    name: str = None
    photo_url: str = None
