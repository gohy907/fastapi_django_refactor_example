import uuid

from pydantic import BaseModel
from datetime import datetime

from schemas.categories import Category


class PostBase(BaseModel):
    text: str
    datetime_to_publish: datetime
    category_id: uuid.UUID


class PostCreate(PostBase):
    author_id: uuid.UUID


class PostUpdate(BaseModel):
    text: str | None = None
    category_id: uuid.UUID | None = None
    datetime_to_publish: datetime | None = None


class Post(BaseModel):
    id: uuid.UUID
    author_id: uuid.UUID
    category: Category
    text: str
    datetime_to_publish: datetime
    created_at: datetime
