# import uuid
# from datetime import datetime
#
# from sqlalchemy import func, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column
#
# from core.db import Base
#
#
# class Post(Base):
#     __tablename__ = "posts"
#
#     id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
#     author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
#     cate
#     datetime_to_publish: Mapped[datetime] = mapped_column()
#
