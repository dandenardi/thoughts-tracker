from fastapi import FastAPI
from app.routes import emotions
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

app.include_router(emotions.router, prefix="/emotions")
