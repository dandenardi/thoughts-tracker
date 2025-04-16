import os
import json
import firebase_admin
from firebase_admin import credentials, auth
from app.config.env import is_production

if not firebase_admin._apps:
    # Railway: tenta carregar config do FIREBASE_CONFIG (variável JSON)
    if is_production():
        firebase_config_json = os.getenv("FIREBASE_CONFIG")
        cred = credentials.Certificate(json.loads(firebase_config_json))
        
    
    else:
        cred_path = os.getenv("FIREBASE_CREDENTIALS")
        cred = credentials.Certificate(cred_path)

    firebase_admin.initialize_app(cred)