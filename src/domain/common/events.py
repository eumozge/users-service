from abc import ABC
from dataclasses import KW_ONLY, dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Event(ABC):
    _: KW_ONLY
    event_id: UUID = field(init=False, default_factory=uuid4)
    event_timestamp: datetime = field(init=False, default_factory=lambda: datetime.now(UTC))
