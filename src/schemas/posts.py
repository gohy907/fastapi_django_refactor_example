import uuid

from pydantic import BaseModel
from datetime import datetime

from schemas.categories import Category


class PostBase(BaseModel):
    title: str
    body: str
    datetime_to_publish: datetime
    category_id: uuid.UUID


class PostCreate(PostBase):
    author_id: uuid.UUID


class PostUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    category_id: uuid.UUID | None = None
    datetime_to_publish: datetime | None = None


class Post(BaseModel):
    id: uuid.UUID
    author_id: uuid.UUID
    category: Category
    datetime_to_publish: datetime
    title: str
    body: str
    created_at: datetime
