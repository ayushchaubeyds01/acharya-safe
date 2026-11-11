
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserRegister(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone_number: str = Field(min_length=10, max_length=20)
    password: str = Field(min_length=8, max_length=128)


class EmailLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    phone_number: str
    role: str
    is_email_verified: bool
    is_phone_verified: bool
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MobileOTPRequest(BaseModel):
    phone_number: str = Field(min_length=10, max_length=20)


class MobileOTPVerify(BaseModel):
    phone_number: str = Field(min_length=10, max_length=20)
    otp: str = Field(pattern=r"^\d{6}$")
