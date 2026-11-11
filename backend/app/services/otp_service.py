
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.otp import generate_otp, hash_otp, verify_otp
from app.models.otp import OTPChallenge
from app.models.user import User
from app.services.sms_service import send_otp_sms


def create_otp_challenge(db: Session, user_id) -> str:
    """Create a new OTP challenge and invalidate previous challenges."""

    current_time = datetime.now(timezone.utc)

    # Find the registered user's phone number.
    user = db.get(User, user_id)

    if user is None:
        raise ValueError("User not found")

    # Invalidate all previous unused OTP challenges.
    db.execute(
        update(OTPChallenge)
        .where(
            OTPChallenge.user_id == user_id,
            OTPChallenge.consumed_at.is_(None)
        )
        .values(consumed_at=current_time)
    )

    # Generate and hash the new OTP.
    otp = generate_otp()
    hashed_otp = hash_otp(otp)

    # Set OTP expiration time.
    expires_at = current_time + timedelta(
        minutes=settings.OTP_EXPIRE_MINUTES
    )

    # Create the new OTP challenge.
    challenge = OTPChallenge(
        user_id=user_id,
        otp_hash=hashed_otp,
        expires_at=expires_at
    )

    try:
        db.add(challenge)
        db.flush()

        # Send OTP through the development SMS service.
        delivery_successful = send_otp_sms(
            user.phone_number,
            otp
        )

        if not delivery_successful:
            raise RuntimeError("OTP delivery failed")

        db.commit()

    except Exception:
        db.rollback()
        raise

    return otp


def verify_otp_challenge(
    db: Session,
    user_id,
    submitted_otp: str
) -> bool:
    """Verify an OTP with expiry, attempt limits, and single-use protection."""

    current_time = datetime.now(timezone.utc)

    # Fetch the latest unused challenge and lock its database row.
    challenge = db.scalar(
        select(OTPChallenge)
        .where(
            OTPChallenge.user_id == user_id,
            OTPChallenge.consumed_at.is_(None)
        )
        .order_by(OTPChallenge.created_at.desc())
        .limit(1)
        .with_for_update()
    )

    if challenge is None:
        return False

    # Reject expired OTPs.
    if challenge.expires_at <= current_time:
        challenge.consumed_at = current_time
        db.commit()
        return False

    # Reject challenges that have exhausted their attempts.
    if challenge.attempts >= settings.OTP_MAX_ATTEMPTS:
        challenge.consumed_at = current_time
        db.commit()
        return False

    # Check the submitted OTP against its stored hash.
    if not verify_otp(submitted_otp, challenge.otp_hash):
        challenge.attempts += 1

        # Invalidate after the maximum number of failed attempts.
        if challenge.attempts >= settings.OTP_MAX_ATTEMPTS:
            challenge.consumed_at = current_time

        db.commit()
        return False

    # Consume the OTP after successful verification.
    challenge.consumed_at = current_time
    db.commit()

    return True
