from datetime import UTC, datetime
from typing import NewType
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy import ForeignKey, insert, types
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sqla.engine import get_engine

String50 = NewType("String50", str)
UserId = NewType("UserId", UUID)
BookId = NewType("BookId", UUID)


class Base(DeclarativeBase):
    type_annotation_map = {
        BookId: types.UUID,
        UserId: types.UUID,
        datetime: types.DateTime(timezone=True),
        String50: types.String(length=50),
    }


class User(Base):
    __tablename__ = "Users"

    id: Mapped[UserId] = mapped_column(primary_key=True)
    username: Mapped[String50] = mapped_column()
    email: Mapped[str | None] = mapped_column()
    password: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(types.DateTime(timezone=True))

    # implicit relationship (DONT! )
    # books: Mapped[list["Book"]] = relationship()


class Book(Base):
    __tablename__ = "Books"

    id: Mapped[BookId] = mapped_column(primary_key=True)

    # explicit relationship
    author_id: Mapped[UserId] = mapped_column(ForeignKey("Users.id"))
    title: Mapped[String50] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()


async def insert_objects(conn: AsyncConnection):
    user_id = UserId(uuid4())
    query = (
        insert(User)
        .values(
            {
                User.id: user_id,
                User.username: "john",
                User.email: "john@gmail.com",
                User.password: "password",
                User.created_at: sa.func.now(),
            }
        )
        .returning(User.id)
    )

    query2 = (
        insert(Book)
        .values(
            {
                Book.id: uuid4(),
                Book.author_id: user_id,
                Book.title: "The Book",
                Book.created_at: datetime.now(UTC),
            }
        )
        .returning(Book.id)
    )

    result = (await conn.execute(query)).first()
    assert result is not None

    result2 = (await conn.execute(query2)).first()
    assert result2 is not None
    book_id: BookId = result2._tuple()[0]


async def fn():
    engine = get_engine()
    async with engine.begin() as conn:
        # await insert_objects(conn)
        # await conn.run_sync(Base.metadata.drop_all)
        # await conn.run_sync(Base.metadata.create_all)
        query = (
            sa.select(
                sa.func.count(User.id).label("BookCountPerAuthor"),
                User.username.label("Author"),
            )
            .select_from(User)
            .join(Book, User.id == Book.author_id)
            .group_by(User.id)
            .limit(10)
        )

        result = (await conn.execute(query)).all()
        print([row._tuple() for row in result])


if __name__ == "__main__":
    import asyncio

    asyncio.run(fn())
