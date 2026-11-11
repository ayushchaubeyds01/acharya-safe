
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.incidents.model import Incident
from app.modules.incidents.schemas.incident import IncidentCreate


def create_incident(
    db: Session,
    user_id: UUID,
    incident_data: IncidentCreate
) -> Incident:
    incident = Incident(
        user_id=user_id,
        activation_source=incident_data.activation_source,
        severity=incident_data.severity,
        status=incident_data.status,
        description=incident_data.description,
        location=incident_data.location
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


def get_user_incidents(
    db: Session,
    user_id: UUID
) -> list[Incident]:
    statement = (
        select(Incident)
        .where(Incident.user_id == user_id)
        .order_by(Incident.started_at.desc())
    )

    return list(db.scalars(statement).all())


def get_incident_by_id(
    db: Session,
    user_id: UUID,
    incident_id: UUID
) -> Incident | None:
    statement = select(Incident).where(
        Incident.id == incident_id,
        Incident.user_id == user_id
    )

    return db.scalar(statement)