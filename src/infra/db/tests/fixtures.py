from collections.abc import AsyncGenerator

import pytest
from domain.users import entities
from domain.users.value_objects.user_id import UserId
from domain.users.value_objects.username import Username
from infra.db.main import get_sa_engine, get_sa_session_maker
from infra.db.models.base import BaseModel
from infra.db.repositories.users import UserRepositoryImpl
from infra.db.tests.factories import AsyncSQLAlchemyModelFactory, UserFactory
from settings import settings
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


@pytest.fixture(autouse=True)
async def _factories(session: AsyncSession) -> None:
    for cls in AsyncSQLAlchemyModelFactory.__subclasses__():
        cls._meta.__dict__["sqlalchemy_session"] = session


@pytest.fixture()
async def user_repository(session: AsyncSession) -> UserRepositoryImpl:
    return UserRepositoryImpl(session)


@pytest.fixture()
async def user() -> entities.User:
    user = UserFactory()
    return entities.User(id=UserId(user.id), username=Username(user.username))
