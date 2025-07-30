from dataclasses import dataclass

from domain.common.exceptions import DomainError


@dataclass(eq=False)
class UsernameAlreadyExistsError(DomainError):
    username: str
