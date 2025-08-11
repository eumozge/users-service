from dataclasses import dataclass
from uuid import UUID

from infra.event_bus.exchanges import USERS_EXCHANGE

from .base import IntegrationEvent, assemble_event


@dataclass(frozen=True)
@assemble_event("UserCreated", exchange=USERS_EXCHANGE)
class UserCreated(IntegrationEvent):
    user_id: UUID
    username: str
