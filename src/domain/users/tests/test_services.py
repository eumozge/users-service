import pytest
from domain.users.entities import User
from domain.users.events import UserCreated
from domain.users.exeptions import UsernameAlreadyExistsError
from domain.users.services import UserService
from domain.users.tests.utils import DummyUserRepository
from domain.users.value_objects.user_id import UserId
from domain.users.value_objects.username import Username


class TestUserService:
    @pytest.fixture()
    def service(self) -> UserService:
        return UserService(user_repository=DummyUserRepository())

    async def test_create_user(self, service: UserService) -> None:
        user = await service.create_user(user_id=UserId(), username=Username("username"))
        event = service.get_events()[0]
        assert isinstance(event, UserCreated)
        assert event.user_id == user.id.to_representative()
        assert event.username == user.username.to_representative()

    async def test_create_user__exists(self, service: UserService) -> None:
        user = User(id=UserId(), username=Username("username"))
        await service.user_repository.create_user(user)

        with pytest.raises(UsernameAlreadyExistsError):
            await service.create_user(user_id=user.id, username=user.username)
