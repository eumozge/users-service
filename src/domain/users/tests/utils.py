from dataclasses import dataclass, field

from domain.users import entities
from domain.users.repositories import UserRepository
from domain.users.value_objects.user_id import UserId
from domain.users.value_objects.username import Username


@dataclass
class DummyUserRepository(UserRepository):
    storage: dict[UserId, entities.User] = field(default_factory=dict)

    def __str__(self) -> str:
        return str(self.storage)

    async def get_user_by_id(self, user_id: UserId) -> entities.User:
        return self.storage[user_id]

    async def check_username_exists(self, username: Username) -> bool:
        return username in {u.username for u in self.storage.values()}

    async def create_user(self, user: entities.User) -> entities.User:
        self.storage[user.id] = user
        return user
