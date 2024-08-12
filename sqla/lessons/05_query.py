import typing
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, async_sessionmaker

from sqla.engine import get_engine
from sqla.models import Book, User, UserId


async def fn():
    engine = get_engine()
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    async with sessionmaker.begin() as session:
        query = sa.select(User).where(User.username == "john2")
        result: list[User] = list((await session.scalars(query)).all())

        query2 = (
            sa.select(User, Book)
            .select_from(User)
            .join(Book, User.id == Book.author_id)
        )
        result2 = (await session.scalars(query2)).all()
        result3 = (await session.execute(query2)).all()

        # wrong type!
        query3: sa.Select[tuple[User, Book]] = (
            sa.select(User, Book)
            .select_from(User)
            .outerjoin(Book, User.id == Book.author_id)
        )
        aliased_query = typing.cast(sa.Select[tuple[User, Book | None]], query3)

        # Correct type -> sa.Select[tuple[User, Book | None]]
        result4 = (await session.scalars(query3)).all()


async def rollback_and_expire_example():
    engine = get_engine()
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    async with sessionmaker.begin() as session:
        # await insert_user_with_session(session)
        # session.expunge_all()

        query = sa.select(User).where(User.username == "john2")
        result = (await session.execute(query)).first()
        assert result is not None
        first_row = result._tuple()[0]

        session.expire(first_row)
        await session.refresh(first_row)
        print(first_row)

        await session.rollback()

    print(first_row)


async def expunge_and_query():
    engine = get_engine()
    sessionmaker = async_sessionmaker(engine)

    async with sessionmaker.begin() as session:
        query = sa.select(User).where(User.username == "mani")
        result = (await session.execute(query)).first()
        assert result is not None
        first_row = result._tuple()[0]
        session.expunge_all()
        first_row.username = "mani2"
        await session.flush()

    print(first_row)


async def insert_user_with_session(session: AsyncSession):
    user = User(
        username="john2",
        password="password",
        created_at=datetime.now(UTC),
        first_name="John",
        last_name="Doe",
    )
    session.add(user)


async def insert_user_with_engine(conn: AsyncConnection):
    query = (
        sa.insert(User)
        .values(
            {
                User.id: UserId(uuid4()),
                User.username: "john1",
                User.password: "password",
                User.created_at: datetime.now(UTC),
                User.first_name: "John",
                User.last_name: "Doe",
            }
        )
        .returning(User.id)
    )
    await conn.execute(query)


if __name__ == "__main__":
    import asyncio

    asyncio.run(fn())
