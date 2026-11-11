
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.token import create_refresh_token, hash_refresh_token
from app.models.refresh_session import RefreshSession
from app.models.user import User


def create_refresh_session(
    db: Session,
    user_id: uuid.UUID
) -> str:
    """Create a new independent login session."""

    current_time = datetime.now(timezone.utc)
    refresh_token = create_refresh_token()

    session = RefreshSession(
        session_id=uuid.uuid4(),
        user_id=user_id,
        token_hash=hash_refresh_token(refresh_token),
        expires_at=current_time + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    )

    try:
        db.add(session)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return refresh_token


def rotate_refresh_session(
    db: Session,
    refresh_token: str
) -> tuple[str, User] | None:
    """Validate and rotate a refresh token."""

    current_time = datetime.now(timezone.utc)
    token_hash = hash_refresh_token(refresh_token)

    token_record = db.scalar(
        select(RefreshSession)
        .where(RefreshSession.token_hash == token_hash)
        .with_for_update()
    )

    if token_record is None:
        return None

    # Reuse of an old or revoked token invalidates the entire session.
    if (
        token_record.used_at is not None
        or token_record.revoked_at is not None
    ):
        db.execute(
            update(RefreshSession)
            .where(
                RefreshSession.session_id == token_record.session_id,
                RefreshSession.revoked_at.is_(None)
            )
            .values(revoked_at=current_time)
        )
        db.commit()
        return None

    expires_at = token_record.expires_at

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at <= current_time:
        token_record.revoked_at = current_time
        db.commit()
        return None

    user = db.get(User, token_record.user_id)

    if user is None or not user.is_active:
        token_record.revoked_at = current_time
        db.commit()
        return None

    new_refresh_token = create_refresh_token()

    token_record.used_at = current_time

    replacement = RefreshSession(
        session_id=token_record.session_id,
        user_id=token_record.user_id,
        token_hash=hash_refresh_token(new_refresh_token),
        expires_at=current_time + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    )

    try:
        db.add(replacement)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return new_refresh_token, user


def revoke_refresh_session(
    db: Session,
    refresh_token: str
) -> None:
    """Revoke the entire login session associated with a refresh token."""

    token_hash = hash_refresh_token(refresh_token)

    token_record = db.scalar(
        select(RefreshSession).where(
            RefreshSession.token_hash == token_hash
        )
    )

    if token_record is None:
        return

    current_time = datetime.now(timezone.utc)

    db.execute(
        update(RefreshSession)
        .where(
            RefreshSession.session_id == token_record.session_id,
            RefreshSession.revoked_at.is_(None)
        )
        .values(revoked_at=current_time)
    )

    db.commit()