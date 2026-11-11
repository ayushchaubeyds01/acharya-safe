
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EmergencyContactCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    phone_number: str = Field(min_length=1, max_length=20)
    relationship: str = Field(min_length=1, max_length=50)


class EmergencyContactUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    phone_number: str | None = Field(default=None, min_length=1, max_length=20)
    relationship: str | None = Field(default=None, min_length=1, max_length=50)


class EmergencyContactResponse(BaseModel):
    id: UUID
    name: str
    phone_number: str
    relationship: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)