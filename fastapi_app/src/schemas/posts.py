from typing import Optional
from pydantic import BaseModel

from datetime import datetime

from schemas.users import User
from schemas.categories import Category


class PostBase(BaseModel):
    text: str
    datetime_to_publish: datetime
    category_id: int


class PostCreate(PostBase):
    author_id: int


class PostUpdate(BaseModel):
    text: Optional[str]
    category_id: Optional[int]
    datetime_to_publish: Optional[datetime]


class Post(BaseModel):
    id: int
    author: User
    category: Category
    text: str
    datetime_to_publish: datetime
    created_at: datetime
