import os
import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv

load_dotenv()

firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS")


if firebase_credentials_path is None:
    raise ValueError("Firebase credentials path is not set in the environment variables")

cred = credentials.Certificate(firebase_credentials_path)
firebase_admin.initialize_app(cred)

