from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from domain.common.events import Event

E = TypeVar("E", bound=Event)


class EventHandler(ABC, Generic[E]):
    @abstractmethod
    async def __call__(self, event: E) -> Any: ...
