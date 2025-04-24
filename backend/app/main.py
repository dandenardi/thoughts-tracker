from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import emotions
from app.routes import symptoms
from app.routes import auth
from app.routes import thoughts
from app.config import firebase_config  # Import Firebase config to initialize the SDK

app = FastAPI(redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    print("PRINTS FUNCIONAM?!")
    return {"message": "Hello World"}

app.include_router(emotions.router, prefix="/emotions")
app.include_router(symptoms.router, prefix="/symptoms")
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(thoughts.router, prefix="/thought-records")
