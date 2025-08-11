from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import ClassVar, TypeVar
from uuid import UUID, uuid4


@dataclass(frozen=True, kw_only=True)
class IntegrationEvent:
    event_id: UUID = field(default_factory=uuid4)
    event_timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    event_type: ClassVar[str]
    exchange_name: ClassVar[str]
    routing_key: ClassVar[str]


EventType = TypeVar("EventType", bound=type[IntegrationEvent])


def assemble_event(
    event_type: str,
    exchange: str,
    routing_key: str | None = None,
) -> Callable[[EventType], EventType]:
    def wrapper(cls: EventType) -> EventType:
        cls.event_type = event_type
        cls.exchange_name = exchange
        cls.routing_key = routing_key if routing_key is not None else event_type
        return cls

    return wrapper
