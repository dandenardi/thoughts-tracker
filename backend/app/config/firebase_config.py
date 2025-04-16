import os
import json
import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv

load_dotenv()  # Isso é útil apenas localmente

# Verifica se o app ainda não foi inicializado
if not firebase_admin._apps:
    # Railway: tenta carregar config do FIREBASE_CONFIG (variável JSON)
    if os.getenv("FIREBASE_CONFIG"):
        firebase_config_json = os.getenv("FIREBASE_CONFIG")
        cred = credentials.Certificate(json.loads(firebase_config_json))
        firebase_admin.initialize_app(cred)
    # Local: usa caminho do arquivo .json
    elif os.getenv("FIREBASE_CREDENTIALS"):
        cred_path = os.getenv("FIREBASE_CREDENTIALS")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    else:
        raise ValueError("Nenhuma configuração de credenciais Firebase foi fornecida.")
