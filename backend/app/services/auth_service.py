
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.core.token import create_access_token
from app.models.user import User
from app.schemas.auth import UserRegister
from app.services.otp_service import verify_otp_challenge


def register_user(db: Session, user_data: UserRegister) -> User:
    """Register a new user."""

    existing_user = db.scalar(
        select(User).where(
            (User.email == user_data.email)
            | (User.phone_number == user_data.phone_number)
        )
    )

    if existing_user:
        raise ValueError("Email or phone number is already registered")

    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        phone_number=user_data.phone_number,
        hashed_password=hash_password(user_data.password)
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()
        raise ValueError("Email or phone number is already registered")

    return new_user


def authenticate_email_user(
    db: Session,
    email: str,
    password: str
) -> User | None:
    """Authenticate a user using email and password."""

    user = db.scalar(
        select(User).where(User.email == email)
    )

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    if not user.is_active:
        return None

    return user


def authenticate_mobile_user(
    db: Session,
    phone_number: str,
    otp: str
) -> User | None:
    """Authenticate an existing user using mobile OTP."""

    user = db.scalar(
        select(User).where(User.phone_number == phone_number)
    )

    if not user or not user.is_active:
        return None

    if not verify_otp_challenge(db, user.id, otp):
        return None

    return user


def create_user_access_token(user: User) -> str:
    """Generate an access token for an authenticated user."""

    return create_access_token(str(user.id))
