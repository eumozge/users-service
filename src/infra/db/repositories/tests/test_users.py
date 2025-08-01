import pytest
from domain.users import entities
from domain.users.value_objects import UserId, Username
from infra.db.repositories.users import UserRepositoryImpl
from sqlalchemy.ext.asyncio import AsyncSession


class TestUserRepositoryImpl:
    @pytest.fixture()
    def repo(self, session: AsyncSession) -> UserRepositoryImpl:
        return UserRepositoryImpl(session)

    async def test_get_user_by_id(self, repo: UserRepositoryImpl) -> None:
        """TODO Tested in `test_create_user`."""

    async def test_check_username_exists(self) -> None:
        """TODO Tested in `test_create_user`."""

    async def test_create_user(self, repo: UserRepositoryImpl) -> None:
        username = Username("username")
        user_id = UserId()
        user = entities.User(id=user_id, username=username)

        assert not await repo.get_user_by_id(user_id)
        assert not await repo.check_username_exists(username)

        await repo.create_user(user)
        await repo.session.commit()

        assert await repo.get_user_by_id(user_id)
        assert await repo.check_username_exists(username)
