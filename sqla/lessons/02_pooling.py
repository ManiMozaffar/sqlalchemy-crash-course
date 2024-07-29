from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


async def fn():
    engine = create_async_engine(
        "postgresql+asyncpg://admin:admin@localhost:5440/learn",
        pool_size=3,
        max_overflow=0,
    )
    now = datetime.now()
    task1 = asyncio.create_task(unit_of_work(engine, name="Task 1"))
    task2 = asyncio.create_task(unit_of_work(engine, name="Task 2"))
    task3 = asyncio.create_task(unit_of_work(engine, name="Task 3"))
    task4 = asyncio.create_task(unit_of_work(engine, name="Task 4"))
    result = await asyncio.gather(task1, task2, task3, task4, return_exceptions=True)
    seconds = datetime.now() - now
    print(f"Result took {seconds.total_seconds()} seconds")
    print(result)


async def unit_of_work(engine: AsyncEngine, name: str):
    async with engine.begin() as transaction:
        query = sa.select(sa.literal(1))
        await transaction.execute(query)
        await asyncio.sleep(2)
        await transaction.commit()
        print(f"OK {name}")
    return name


if __name__ == "__main__":
    import asyncio

    asyncio.run(fn())
