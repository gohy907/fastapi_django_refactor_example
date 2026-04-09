import uuid
from pydantic import BaseModel, SecretStr, ConfigDict, field_validator
from datetime import datetime

import re

class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    password: SecretStr
    @field_validator("password", mode="after")
    @classmethod
    def password_complexity(cls, v: SecretStr):
        password = v.get_secret_value()
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[a-zA-Z]", password):
            raise ValueError("Password must contain at least one letter.")
        return v


class UserUpdate(BaseModel):
    login: str | None = None
    password: str | None = None


class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
