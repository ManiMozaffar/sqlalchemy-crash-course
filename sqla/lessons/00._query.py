import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg_dialect

if __name__ == "__main__":
    query = sa.select(sa.literal(1), sa.literal(2), sa.literal(3))
    pg = pg_dialect.dialect()
    print(query.compile(dialect=pg, compile_kwargs={"literal_binds": True}))
