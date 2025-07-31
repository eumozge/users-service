from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import orjson
from infra.settings import settings
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine


@asynccontextmanager
async def get_sa_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        settings.db.asyncurl,
        echo=False,
        json_serializer=lambda data: orjson.dumps(data).decode(),
        json_deserializer=orjson.loads,
        pool_size=50,
    )
    yield engine

    await engine.dispose()


def get_sa_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
