from collections.abc import AsyncGenerator

import pytest
from infra.db.main import get_sa_engine, get_sa_session_maker
from infra.db.models.base import BaseModel
from infra.settings import settings
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


@pytest.fixture()
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    async with get_sa_engine(settings.db.asyncurl) as engine:
        async with engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)
            await conn.run_sync(BaseModel.metadata.create_all)

        yield engine

        async with engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)


@pytest.fixture()
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    async_session = get_sa_session_maker(engine)

    async with async_session() as session:
        yield session
