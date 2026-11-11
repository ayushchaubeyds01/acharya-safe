
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.models.user import User
from app.modules.incidents.schemas.incident import IncidentResponse
from app.modules.incidents.services.incident_service import (
    get_user_incidents,
    get_incident_by_id,
)


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


@router.get(
    "",
    response_model=list[IncidentResponse]
)
def list_incidents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_user_incidents(db, current_user.id)


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse
)
def retrieve_incident(
    incident_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    incident = get_incident_by_id(
        db,
        current_user.id,
        incident_id
    )

    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found"
        )

    return incident