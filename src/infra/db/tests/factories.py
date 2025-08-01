import uuid
from typing import Any, Generic, TypeVar

import factory
from factory.alchemy import SQLAlchemyModelFactory
from infra.db.models.users import UserModel

T = TypeVar("T")


class AsyncSQLAlchemyModelFactory(SQLAlchemyModelFactory, Generic[T]):
    @classmethod
    async def _create(cls, model_class: type[T], *args: Any, **kwargs: Any) -> T:
        instance = super()._create(model_class, *args, **kwargs)
        async with cls._meta.sqlalchemy_session as session:
            await session.commit()
        return instance


class UserFactory(AsyncSQLAlchemyModelFactory[UserModel]):
    id = factory.LazyFunction(uuid.uuid4)
    username = factory.Faker("user_name")

    class Meta:
        model = UserModel
        sqlalchemy_session_persistence = "commit"
