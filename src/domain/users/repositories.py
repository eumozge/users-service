from abc import ABC, abstractmethod

from domain.users import entities
from domain.users.value_objects.user_id import UserId
from domain.users.value_objects.username import Username


class UserRepository(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: UserId) -> entities.User | None: ...

    @abstractmethod
    async def check_username_exists(self, username: Username) -> bool: ...

    @abstractmethod
    async def create_user(self, user: entities.User) -> None: ...
