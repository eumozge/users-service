from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True, eq=False)
class AppError(Exception):
    status: ClassVar[int] = 500


@dataclass(frozen=True, eq=False)
class DomainError(AppError):
    pass
