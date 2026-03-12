import uuid
from pydantic import BaseModel, SecretStr
from datetime import datetime


class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    password: SecretStr


class UserUpdate(BaseModel):
    login: str | None = None
    password: str | None = None


class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime
