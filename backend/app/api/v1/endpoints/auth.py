
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.auth import (
    UserRegister,
    UserResponse,
    EmailLogin,
    TokenResponse,
    MobileOTPRequest,
    MobileOTPVerify
)
from app.services.auth_service import (
    register_user,
    authenticate_email_user,
    authenticate_mobile_user,
    create_user_access_token
)
from app.services.otp_service import create_otp_challenge


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    try:
        return register_user(db, user_data)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        ) from error


@router.post(
    "/login/email",
    response_model=TokenResponse
)
def email_login(
    login_data: EmailLogin,
    db: Session = Depends(get_db)
):
    user = authenticate_email_user(
        db,
        login_data.email,
        login_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_user_access_token(user)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )


@router.post(
    "/login/mobile/request-otp"
)
def request_mobile_otp(
    request_data: MobileOTPRequest,
    db: Session = Depends(get_db)
):
    user = db.scalar(
        select(User).where(
            User.phone_number == request_data.phone_number
        )
    )

    # Only existing active users can request an OTP.
    if user and user.is_active:
        create_otp_challenge(db, user.id)

    # Use the same response for registered and unregistered numbers.
    return {
        "message": "If this phone number is registered, an OTP has been sent."
    }


@router.post(
    "/login/mobile/verify-otp",
    response_model=TokenResponse
)
def verify_mobile_otp(
    verification_data: MobileOTPVerify,
    db: Session = Depends(get_db)
):
    user = authenticate_mobile_user(
        db,
        verification_data.phone_number,
        verification_data.otp
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired OTP"
        )

    access_token = create_user_access_token(user)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )


@router.get(
    "/me",
    response_model=UserResponse
)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user
