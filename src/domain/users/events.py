from dataclasses import dataclass
from uuid import UUID

from domain.common.events import Event


@dataclass(frozen=True)
class UserCreated(Event):
    user_id: UUID
    username: str
