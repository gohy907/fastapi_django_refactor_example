import uuid

from datetime import datetime
from pydantic import BaseModel, ConfigDict


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


class PostResponse(PostBase):
    id: uuid.UUID
    author_id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
