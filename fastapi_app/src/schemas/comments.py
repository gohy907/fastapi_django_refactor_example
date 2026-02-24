from pydantic import BaseModel, date
from posts import Post
from users import User


class CommentRequestSchema(BaseModel):
    text: str
    post: Post
    author: User


class CommentResponseSchema(BaseModel):
    text: str
    post: Post
    author: User
    created_at: date
