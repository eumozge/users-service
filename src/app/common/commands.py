from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

CRes = TypeVar("CRes")


@dataclass(eq=False, frozen=True)
class Command(ABC, Generic[CRes]):
    pass


CReq = TypeVar("CReq", bound=Command[Any])


class CommandHandler(ABC, Generic[CReq, CRes]):
    @abstractmethod
    def __call__(self, command: CReq) -> CRes: ...
