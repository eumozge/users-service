from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

CRes = TypeVar("CRes")


@dataclass(eq=False, frozen=True)
class Command(ABC, Generic[CRes]):
    pass


CReq = TypeVar("CReq", bound=Command[Any])


class CommandHandler(ABC, Generic[CReq, CRes]):
    @abstractmethod
    async def __call__(self, command: CReq) -> CRes: ...


@dataclass(eq=False)
class CommandDispatcher(ABC):
    handlers: dict[type[Command], type[CommandHandler]] = field(default_factory=dict)

    @abstractmethod
    def register_handler(self, command: type[Command[CRes]], handler: type[CommandHandler[CReq, CRes]]) -> None: ...

    @abstractmethod
    async def send(self, command: Command[CRes], *args: Any, **kwargs: Any) -> CRes: ...


@dataclass(eq=False)
class CommandDispatcherImpl(CommandDispatcher):
    def register_handler(self, command: type[Command[CRes]], handler: type[CommandHandler[CReq, CRes]]) -> None:
        self.handlers[command] = handler

    async def send(self, command: Command[CRes], *args: Any, **kwargs: Any) -> CRes:
        handler = self.handlers[command.__class__](*args, **kwargs)
        return await handler(command)
