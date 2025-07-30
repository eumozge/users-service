from dataclasses import dataclass

from domain.common.services import BaseService
from domain.users import entities
from domain.users.events import UserCreated
from domain.users.exeptions import UsernameAlreadyExistsError
from domain.users.repositories import UserRepository
from domain.users.value_objects.user_id import UserId
from domain.users.value_objects.username import Username


@dataclass(eq=False)
class UserService(BaseService):
    user_repository: UserRepository

    async def create_user(self, user_id: UserId, username: Username) -> entities.User:
        if await self.user_repository.check_username_exists(username):
            raise UsernameAlreadyExistsError(username.value)

        user = entities.User(id=user_id, username=username)
        await self.user_repository.create_user(user)

        event = UserCreated(user_id=user_id.to_representative(), username=username.to_representative())
        self.register_event(event)
        return user
