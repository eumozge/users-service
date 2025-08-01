from dataclasses import dataclass

from domain.common.entities import Entity
from domain.users.value_objects.user_id import UserId
from domain.users.value_objects.username import Username


@dataclass
class User(Entity):
    id: UserId
    username: Username
