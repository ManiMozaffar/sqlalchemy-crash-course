from sqla.engine import get_engine
from sqla.models import *  # noqa
from sqla.models import Base


async def fn():
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    import asyncio

    asyncio.run(fn())
