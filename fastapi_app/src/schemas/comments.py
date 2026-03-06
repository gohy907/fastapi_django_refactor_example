import uuid

from pydantic import BaseModel
from datetime import datetime


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    author_id: uuid.UUID
    post_id: uuid.UUID


class CommentUpdate(BaseModel):
    text: str | None = None


class Comment(BaseModel):
    author_id: uuid.UUID
    post_id: uuid.UUID
    text: str
    created_at: datetime
