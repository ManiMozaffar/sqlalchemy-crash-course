from functools import lru_cache

from sqlalchemy.ext.asyncio import create_async_engine


@lru_cache
def get_engine():
    engine = create_async_engine(
        "postgresql+asyncpg://admin:admin@localhost:5440/learn",
        echo=True,
        pool_size=1,
        max_overflow=0,
    )
    return engine
