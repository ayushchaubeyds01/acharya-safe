
from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


ActivationSource = Literal["voice", "movement", "manual"]
IncidentSeverity = Literal["critical", "high", "medium", "low", "unknown"]
IncidentStatus = Literal[
    "detected",
    "investigating",
    "responding",
    "resolved",
    "false_alarm"
]


class IncidentCreate(BaseModel):
    activation_source: ActivationSource
    severity: IncidentSeverity = "unknown"
    status: IncidentStatus = "detected"
    description: str | None = Field(default=None, max_length=5000)
    location: dict[str, Any] | None = None


class IncidentResponse(BaseModel):
    id: UUID
    user_id: UUID
    activation_source: ActivationSource
    severity: IncidentSeverity
    status: IncidentStatus
    description: str | None
    location: dict[str, Any] | None
    started_at: datetime
    resolved_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)