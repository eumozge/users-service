from abc import ABC

from users.domain.common.events import Event


class BaseService(ABC):
    def __init__(self):
        self._events: list[Event] = []

    def register_event(self, event: Event) -> None:
        self._events.append(event)

    def get_events(self) -> list[Event]:
        return self._events
