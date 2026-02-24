from pydantic import BaseModel, Field, date


class CategoryRequestSchema(BaseModel):
    title: str = Field(max_length=256)
    description: str
    is_published: bool


class CategoryResponseSchema(BaseModel):
    title: str = Field(max_length=256)
    description: str
    is_published: bool
    created_at: date
