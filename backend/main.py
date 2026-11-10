
from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="ACHARYA SAFE API",
    description="AI-powered Personal Safety and Emergency Response Platform",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def home():
    return {
        "message": "Welcome to ACHARYA SAFE API",
        "status": "Running"
    }
