
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    JSON,
    String,
    Text,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    __table_args__ = (
        CheckConstraint(
            "activation_source IN ('voice', 'movement', 'manual')",
            name="ck_incidents_activation_source"
        ),
        CheckConstraint(
            "severity IN ('critical', 'high', 'medium', 'low', 'unknown')",
            name="ck_incidents_severity"
        ),
        CheckConstraint(
            "status IN ('detected', 'investigating', 'responding', 'resolved', 'false_alarm')",
            name="ck_incidents_status"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    activation_source: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    severity: Mapped[str] = mapped_column(
        String(20),
        default="unknown",
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="detected",
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    location: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )