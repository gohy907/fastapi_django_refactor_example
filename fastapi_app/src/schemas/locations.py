from pydantic import BaseModel, Field, date
from users import User


class LocationRequestSchema(BaseModel):
    name: str = Field(max_length=256)
    description: str
    author: User
    is_published: bool


class PostResponseSchema(BaseModel):
    title: str = Field(max_length=256)
    description: str
    is_published: bool
    author: User
    created_at: date
