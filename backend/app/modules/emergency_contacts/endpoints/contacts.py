
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.models.user import User
from app.modules.emergency_contacts.schemas.contact import (
    EmergencyContactCreate,
    EmergencyContactUpdate,
    EmergencyContactResponse
)
from app.modules.emergency_contacts.services.contact_service import (
    create_contact,
    get_user_contacts,
    get_contact_by_id,
    update_contact,
    delete_contact
)


router = APIRouter(
    prefix="/emergency-contacts",
    tags=["Emergency Contacts"]
)


@router.post(
    "",
    response_model=EmergencyContactResponse,
    status_code=status.HTTP_201_CREATED
)
def add_emergency_contact(
    contact_data: EmergencyContactCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_contact(db, current_user.id, contact_data)


@router.get(
    "",
    response_model=list[EmergencyContactResponse]
)
def list_emergency_contacts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_user_contacts(db, current_user.id)


@router.get(
    "/{contact_id}",
    response_model=EmergencyContactResponse
)
def retrieve_emergency_contact(
    contact_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    contact = get_contact_by_id(db, current_user.id, contact_id)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency contact not found"
        )

    return contact


@router.patch(
    "/{contact_id}",
    response_model=EmergencyContactResponse
)
def edit_emergency_contact(
    contact_id: UUID,
    contact_data: EmergencyContactUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    contact = get_contact_by_id(db, current_user.id, contact_id)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency contact not found"
        )

    return update_contact(db, contact, contact_data)


@router.delete(
    "/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_emergency_contact(
    contact_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    contact = get_contact_by_id(db, current_user.id, contact_id)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency contact not found"
        )

    delete_contact(db, contact)