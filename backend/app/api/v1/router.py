
from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.modules.emergency_contacts.endpoints.contacts import (
    router as emergency_contacts_router
)

api_router = APIRouter()


api_router.include_router(auth_router)
api_router.include_router(emergency_contacts_router)


@api_router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "ACHARYA SAFE API is working"
    }
