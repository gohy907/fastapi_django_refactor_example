import uuid

from pydantic import BaseModel, Field
from datetime import datetime


class LocationBase(BaseModel):
    title: str = Field(max_length=256)
    description: str
    is_published: bool


class LocationCreate(LocationBase):
    author_id: uuid.UUID


class LocationUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_published: bool | None = None


class Location(BaseModel):
    id: uuid.UUID
    author_id: uuid.UUID
    title: str = Field(max_length=256)
    description: str
    is_published: bool
    created_at: datetime
