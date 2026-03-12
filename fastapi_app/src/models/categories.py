
import uuid
from datetime import datetime

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    is_published: Mapped[bool] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
