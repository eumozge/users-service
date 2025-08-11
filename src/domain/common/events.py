from abc import ABC
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass(frozen=True, kw_only=True)
class Event(ABC):
    event_id: UUID = field(init=False, default_factory=uuid4)
    event_timestamp: datetime = field(init=False, default_factory=lambda: datetime.now(UTC))
