from fastapi import APIRouter, Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.services.auth_service import verify_token
from app.models.users import User

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login")
async def login(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    return {"message": "Login successful", "user": user}

@router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    return {"user": user}

@router.get("/verify-token", response_model=User)
def verify_user(id_token: str):
    return verify_token(id_token)
