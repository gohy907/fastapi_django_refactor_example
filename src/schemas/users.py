from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
from fastapi import HTTPException, status


class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    password: str

    @field_validator("login")
    @classmethod
    def check_login(cls, login: str) -> str:
        if not login.startswith("user_"):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Логин пользователя обязан начинаться с 'user_'"
            )
        return login


class UserResponse(UserBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
