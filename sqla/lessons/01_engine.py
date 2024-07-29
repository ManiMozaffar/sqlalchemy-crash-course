import random

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


async def unit_of_work(engine: AsyncEngine):
    async with engine.begin() as connection:
        query = sa.select(sa.literal(1), sa.literal(2), sa.literal(3))
        await connection.execute(query)

        if random.choice([True, False]):
            raise ValueError("This is a test")

    # Don't raise exception outside of ctx manager if you want to rollback a unit of work!
    # raise ValueError("This is a test")


async def fn():
    engine = create_async_engine(
        "postgresql+asyncpg://admin:admin@localhost:5440/learn", echo=True, pool_size=20
    )

    try:
        await asyncio.gather(unit_of_work(engine), unit_of_work(engine))
        await unit_of_work(engine)
    except Exception:
        ...


if __name__ == "__main__":
    import asyncio

    asyncio.run(fn())
