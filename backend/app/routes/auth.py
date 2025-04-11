from fastapi import APIRouter, Security
from app.dependencies.auth_dependency import get_current_user
from app.models.users import User

router = APIRouter()

@router.get("/me")
async def get_current_user_endpoint(current_user = Security(get_current_user)):
    return {"user": current_user}

@router.get("/verify-token", response_model=User)
async def verify_user_endpoint(current_user = Security(get_current_user)):
    return current_user
