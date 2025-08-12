from collections.abc import AsyncGenerator

import pytest
from domain.users import entities
from domain.users.value_objects.user_id import UserId
from domain.users.value_objects.username import Username
from infra.db.main import get_sa_engine, get_sa_session_maker
from infra.db.models.base import BaseModel
from infra.db.repositories.users import UserRepositoryImpl
from settings import settings
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from tests.db.factories import AsyncSQLAlchemyModelFactory, UserFactory


@pytest.fixture()
async def db_engine() -> AsyncGenerator[AsyncEngine, None]:
    async with get_sa_engine(settings.db.asyncurl) as engine:
        async with engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)
            await conn.run_sync(BaseModel.metadata.create_all)

        yield engine

        async with engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)


@pytest.fixture()
async def db_session(db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    async_session = get_sa_session_maker(db_engine)

    async with async_session() as session:
        yield session


@pytest.fixture(autouse=True)
async def _factories(db_session: AsyncSession) -> None:
    for cls in AsyncSQLAlchemyModelFactory.__subclasses__():
        cls._meta.__dict__["sqlalchemy_session"] = db_session


@pytest.fixture()
async def user_repository(db_session: AsyncSession) -> UserRepositoryImpl:
    return UserRepositoryImpl(db_session)


@pytest.fixture()
async def user() -> entities.User:
    user = UserFactory()
    return entities.User(id=UserId(user.id), username=Username(user.username))
