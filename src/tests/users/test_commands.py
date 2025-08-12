from app.users.commands import CreateUser, CreateUserHandler
from domain.users.entities import User
from domain.users.services import UserService
from domain.users.value_objects import UserId, Username
from infra.db.repositories.users import UserRepositoryImpl
from infra.db.uow import SQLAlchemyUoW


class TestCreateUserHandler:
    async def test(self, user_repository: UserRepositoryImpl) -> None:
        user = User(id=UserId(), username=Username("username"))
        assert not await user_repository.check_username_exists(user.username)

        handler = CreateUserHandler(
            user_service=UserService(user_repository),
            uow=SQLAlchemyUoW(user_repository.session),
        )
        command = CreateUser(user_id=user.id.to_representative(), username=user.username.to_representative())
        await handler(command)

        assert await user_repository.check_username_exists(user.username)
