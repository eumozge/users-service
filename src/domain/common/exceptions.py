from dataclasses import dataclass
from typing import ClassVar


@dataclass(eq=False)
class AppError(Exception):
    status: ClassVar[int] = 500


@dataclass(eq=False)
class DomainError(AppError):
    pass
