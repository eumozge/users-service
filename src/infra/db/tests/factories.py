import uuid
from typing import Any, Self, TypeVar

import factory
from factory.alchemy import SQLAlchemyModelFactory
from infra.db.models.users import UserModel

T = TypeVar("T", bound="AsyncSQLAlchemyModelFactory")


class AsyncSQLAlchemyModelFactory(SQLAlchemyModelFactory):
    @classmethod
    async def _create(cls, model_class: Any, *args: Any, **kwargs: Any) -> Self:
        instance = super()._create(model_class, *args, **kwargs)
        async with cls._meta.sqlalchemy_session as session:
            await session.commit()
        return instance


class UserFactory(AsyncSQLAlchemyModelFactory):
    id = factory.LazyFunction(uuid.uuid4)
    username = factory.Faker("user_name")

    class Meta:
        model = UserModel
        sqlalchemy_session_persistence = "commit"
