import sqlalchemy as sa
from rich import print

from sqla.engine import get_engine


async def fn():
    engine = get_engine()
    async with engine.begin() as transaction:
        query = sa.select(sa.literal(1).label("one"), sa.literal(2).label("two"))
        print(query.compile())

        result = await transaction.execute(query)
        all_result = list(result.all())
        row = all_result[0]
        print("Row `one`: ", row.one)
        print("Dictionary: ", row._asdict())
        print("Tuple: ", row._tuple())

        query = sa.select(sa.literal(3).label("three"), sa.literal(4).label("four"))
        result: sa.CursorResult[tuple[int, int]] = await transaction.execute(query)
        rows: list[sa.Row[tuple[int, int]]] = list(result.all())

        # recommended way: don't use `Row` object directly
        all_tuples = [r._tuple() for r in rows]
        print("All tuples: ", all_tuples)

        all_dicts = [r._asdict() for r in rows]
        print("All dicts: ", all_dicts)


if __name__ == "__main__":
    import asyncio

    asyncio.run(fn())
