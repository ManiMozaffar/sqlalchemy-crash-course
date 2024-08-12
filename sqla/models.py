from datetime import datetime
from typing import NewType
from uuid import UUID as PythonUUID
from uuid import uuid4

from sqlalchemy import types as t
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column
from sqlalchemy.schema import ForeignKeyConstraint, PrimaryKeyConstraint

UserId = NewType("UserId", PythonUUID)
BookId = NewType("BookId", PythonUUID)


class Base(MappedAsDataclass, DeclarativeBase):
    type_annotation_map = {
        BookId: t.UUID,
        UserId: t.UUID,
        datetime: t.DateTime(timezone=True),
    }


class User(Base):
    __tablename__ = "Users"
    __table_args__ = (PrimaryKeyConstraint("id", name="user_pk"),)

    first_name: Mapped[str | None]
    last_name: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[datetime]

    id: Mapped[UserId] = mapped_column(default_factory=uuid4)


class Book(Base):
    __tablename__ = "Books"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="book_pk"),
        ForeignKeyConstraint(["author_id"], ["Users.id"], ondelete="CASCADE"),
    )

    title: Mapped[str]
    author_id: Mapped[UserId]
    id: Mapped[BookId] = mapped_column(default_factory=uuid4)
