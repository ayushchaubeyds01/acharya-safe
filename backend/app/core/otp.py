
import hashlib
import hmac
import secrets
import string

from app.core.config import settings


def generate_otp() -> str:
    """Generate a cryptographically secure numeric OTP."""

    return "".join(
        secrets.choice(string.digits)
        for _ in range(settings.OTP_LENGTH)
    )


def hash_otp(otp: str) -> str:
    """Generate a keyed HMAC hash of an OTP."""

    secret = settings.JWT_SECRET_KEY.encode("utf-8")
    message = f"acharya-safe:otp:{otp}".encode("utf-8")

    return hmac.new(
        secret,
        message,
        hashlib.sha256
    ).hexdigest()


def verify_otp(plain_otp: str, hashed_otp: str) -> bool:
    """Verify an OTP using constant-time comparison."""

    return hmac.compare_digest(
        hash_otp(plain_otp),
        hashed_otp
    )
