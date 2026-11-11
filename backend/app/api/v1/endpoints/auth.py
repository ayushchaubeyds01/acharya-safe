
from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    Header,
    HTTPException,
    Response,
    status
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.core.config import settings
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
from app.services.session_service import (
    create_refresh_session,
    rotate_refresh_session,
    revoke_refresh_session
)


router = APIRouter(prefix="/auth", tags=["Authentication"])


def validate_request_origin(origin: str | None) -> None:
    """Validate the origin of cookie-authenticated requests."""

    if origin not in settings.BACKEND_CORS_ORIGINS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid request origin"
        )


def set_refresh_cookie(
    response: Response,
    refresh_token: str
) -> None:
    """Set the refresh token in an HttpOnly cookie."""

    response.set_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        value=refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        httponly=True,
        secure=settings.REFRESH_COOKIE_SECURE,
        samesite=settings.REFRESH_COOKIE_SAMESITE,
        path=settings.REFRESH_COOKIE_PATH
    )


def clear_refresh_cookie(response: Response) -> None:
    """Clear the refresh cookie using its original path."""

    response.delete_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        httponly=True,
        secure=settings.REFRESH_COOKIE_SECURE,
        samesite=settings.REFRESH_COOKIE_SAMESITE,
        path=settings.REFRESH_COOKIE_PATH
    )


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
    response: Response,
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
    refresh_token = create_refresh_session(db, user.id)

    set_refresh_cookie(response, refresh_token)

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
    response: Response,
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
    refresh_token = create_refresh_session(db, user.id)

    set_refresh_cookie(response, refresh_token)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )


@router.post(
    "/refresh",
    response_model=TokenResponse
)
def refresh_access_token(
    response: Response,
    origin: str | None = Header(default=None, alias="Origin"),
    refresh_token: str | None = Cookie(
        default=None,
        alias=settings.REFRESH_COOKIE_NAME
    ),
    db: Session = Depends(get_db)
):
    validate_request_origin(origin)

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is missing"
        )

    result = rotate_refresh_session(db, refresh_token)

    if result is None:
        clear_refresh_cookie(response)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh session"
        )

    new_refresh_token, user = result
    access_token = create_user_access_token(user)

    set_refresh_cookie(response, new_refresh_token)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )


@router.post(
    "/logout"
)
def logout(
    response: Response,
    origin: str | None = Header(default=None, alias="Origin"),
    refresh_token: str | None = Cookie(
        default=None,
        alias=settings.REFRESH_COOKIE_NAME
    ),
    db: Session = Depends(get_db)
):
    validate_request_origin(origin)

    if refresh_token:
        revoke_refresh_session(db, refresh_token)

    clear_refresh_cookie(response)

    return {
        "message": "Logged out successfully"
    }


@router.get(
    "/me",
    response_model=UserResponse
)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user