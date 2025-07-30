from abc import ABC
from dataclasses import dataclass, field

from domain.common.events import Event


@dataclass(eq=False)
class BaseService(ABC):
    events: list[Event] = field(kw_only=True, default_factory=list)

    def register_event(self, event: Event) -> None:
        self.events.append(event)

    def get_events(self) -> list[Event]:
        return self.events
