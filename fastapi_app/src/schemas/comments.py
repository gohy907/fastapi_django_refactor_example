from pydantic import BaseModel
from datetime import datetime
from typing import Optional


from schemas.posts import Post
from schemas.users import User


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    author_id: int
    post_id: int


class CommentUpdate(BaseModel):
    text: Optional[str]


class Comment(BaseModel):
    author: User
    post: Post
    text: str
    created_at: datetime
