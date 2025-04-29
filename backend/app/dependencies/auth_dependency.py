import asyncio
from fastapi import Request, HTTPException, Security, Depends
from firebase_admin import auth
from fastapi.security import HTTPBearer
from app.models.user import User
from app.services.user_service import get_user_by_firebase_uid, create_user


security = HTTPBearer()

async def get_current_user(request: Request, token: str = Security(security)):
    
    try:
        
        decoded_token = auth.verify_id_token(token.credentials)
    
        uid = decoded_token["uid"]

        
        user = get_user_by_firebase_uid(uid)  # Aqui que deve ser mockado
        

        if not user:
            print("❌ Nenhum usuário encontrado. Criando novo...")
            user = create_user(User(uid=uid, email=decoded_token.get("email"), name=decoded_token.get("name", ""), photo_url=decoded_token.get("picture", "")))
            print(f"✅ Usuário criado: {user}")
        return user

    except Exception as e:
        print(f"⚠️ Erro em get_current_user: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")
