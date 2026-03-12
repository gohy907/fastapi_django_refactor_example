import uuid

from pydantic import BaseModel, Field
from datetime import datetime


class CategoryBase(BaseModel):
    title: str = Field(max_length=256)
    description: str
    is_published: bool


class CategoryCreate(CategoryBase):
    author_id: uuid.UUID


class CategoryUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class CategoryResponse(BaseModel):
    id: uuid.UUID
    author_id: uuid.UUID
    title: str = Field(max_length=256)
    description: str
    created_at: datetime
