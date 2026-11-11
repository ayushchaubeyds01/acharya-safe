
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.emergency_contacts.model import EmergencyContact
from app.modules.emergency_contacts.schemas.contact import (
    EmergencyContactCreate,
    EmergencyContactUpdate
)


def create_contact(
    db: Session,
    user_id: UUID,
    contact_data: EmergencyContactCreate
) -> EmergencyContact:
    contact = EmergencyContact(
        user_id=user_id,
        name=contact_data.name.strip(),
        phone_number=contact_data.phone_number.strip(),
        relationship=contact_data.relationship.strip()
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact


def get_user_contacts(
    db: Session,
    user_id: UUID
) -> list[EmergencyContact]:
    statement = (
        select(EmergencyContact)
        .where(EmergencyContact.user_id == user_id)
        .order_by(EmergencyContact.created_at.desc())
    )

    return list(db.scalars(statement).all())


def get_contact_by_id(
    db: Session,
    user_id: UUID,
    contact_id: UUID
) -> EmergencyContact | None:
    statement = select(EmergencyContact).where(
        EmergencyContact.id == contact_id,
        EmergencyContact.user_id == user_id
    )

    return db.scalar(statement)


def update_contact(
    db: Session,
    contact: EmergencyContact,
    contact_data: EmergencyContactUpdate
) -> EmergencyContact:
    update_data = contact_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if value is not None:
            setattr(contact, field, value.strip())

    db.commit()
    db.refresh(contact)

    return contact


def delete_contact(
    db: Session,
    contact: EmergencyContact
) -> None:
    db.delete(contact)
    db.commit()