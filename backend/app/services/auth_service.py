from firebase_admin import auth
from fastapi import HTTPException, status
from app.models.users import User

def verify_token(id_token: str) -> User:
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]
        user_info = auth.get_user(uid)

        return User(
            uid=uid,
            email=user_info.email,
            name=user_info.display_name,
            photo_url=user_info.photo_url
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid authentication credentials"
        )
    
    
