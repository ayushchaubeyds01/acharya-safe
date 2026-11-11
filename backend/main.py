
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings


app = FastAPI(
    title=f"{settings.APP_NAME} API",
    description="AI-powered Personal Safety and Emergency Response Platform",
    version="1.0.0"
)

# Allow requests from the User and Admin frontends.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX
)


@app.get("/")
def home():
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "status": "Running"
    }
