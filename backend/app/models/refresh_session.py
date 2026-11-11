
import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    String,
    Uuid,
    func
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class RefreshSession(Base):
    __tablename__ = "refresh_sessions"

    __table_args__ = (
        Index(
            "ix_refresh_sessions_session_id",
            "session_id"
        ),
        Index(
            "ix_refresh_sessions_user_id",
            "user_id"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )

    # Groups all rotated tokens belonging to one login session.
    session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # Store only the SHA-256 hash of the refresh token.
    token_hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )