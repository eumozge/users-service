import re
from dataclasses import dataclass

from domain.common.exceptions import DomainError
from domain.common.value_objects import ValueObject

MAX_USERNAME_LENGTH = 32
USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9]+$")


@dataclass(eq=False)
class UsernameValueError(ValueError, DomainError):
    username: str


class EmptyUsernameError(UsernameValueError):
    pass


class TooLongUsernameError(UsernameValueError):
    pass


class WrongUsernameFormatError(UsernameValueError):
    pass


@dataclass(frozen=True)
class Username(ValueObject[str]):
    value: str

    def validate(self) -> None:
        if not len(self.value):
            raise EmptyUsernameError(self.value)
        if len(self.value) > MAX_USERNAME_LENGTH:
            raise TooLongUsernameError(self.value)
        if not USERNAME_PATTERN.match(self.value):
            raise WrongUsernameFormatError(self.value)
