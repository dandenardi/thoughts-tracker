from fastapi import FastAPI
from app.routes import emotions
from app.routes import auth
from app.routes import emotion_records

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

app.include_router(emotions.router, prefix="/emotions")
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(emotion_records.router)
