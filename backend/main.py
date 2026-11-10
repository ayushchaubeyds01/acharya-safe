from fastapi import FastAPI

app = FastAPI(
    title="ACHARYA SAFE API",
    description="AI-powered Personal Safety and Emergency Response Platform",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to ACHARYA SAFE API",
        "status": "Running"
    }
