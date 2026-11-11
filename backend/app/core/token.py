
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt

from app.core.config import settings


def create_access_token(subject: str) -> str:
    """Generate a signed JWT access token."""

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": subject,
        "exp": expires_at,
        "iat": datetime.now(timezone.utc),
        "jti": str(uuid4()),
        "type": "access"
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )


def decode_access_token(token: str) -> dict:
    """Verify and decode a JWT access token."""

    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM]
    )

    if payload.get("type") != "access":
        raise jwt.InvalidTokenError("Invalid token type")

    if not payload.get("sub"):
        raise jwt.InvalidTokenError("Token subject is missing")

    return payload


def create_refresh_token() -> str:
    """Generate a cryptographically secure opaque refresh token."""

    return secrets.token_urlsafe(64)


def hash_refresh_token(token: str) -> str:
    """Generate a SHA-256 hash of a refresh token for database storage."""

    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()