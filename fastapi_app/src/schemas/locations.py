from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


from schemas.users import User


class LocationBase(BaseModel):
    title: str = Field(max_length=256)
    description: str
    is_published: bool


class LocationCreate(LocationBase):
    author_id: int


class LocationUpdate(BaseModel):
    title: Optional[str] = Field(max_length=256)
    description: Optional[str]
    is_published: Optional[bool]


class Location(BaseModel):
    id: int
    author: User
    title: str = Field(max_length=256)
    description: str
    is_published: bool
    created_at: datetime
