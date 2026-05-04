from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
from fastapi import HTTPException, status
from src.resources.auth import get_password_hash


class UserBase(BaseModel):
    login: str


class UserInternal(UserBase):
    password_hash: str


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

    def to_internal(self) -> UserInternal:
        return UserInternal(login=self.login,
                            password_hash=get_password_hash(self.password))


class UserResponse(UserBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    login: str | None
    password: str | None

    def to_internal(self) -> UserInternal:
        data = self.model_dump(exclude_unset=True)

        if "password" in data:
            raw_password = data.pop("password")
            data["password_hash"] = get_password_hash(raw_password)

        return UserInternal(**data)
