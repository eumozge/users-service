from dataclasses import dataclass
from uuid import UUID

from app.common.exceptions import ApplicationError


@dataclass(eq=False)
class UserIdAlreadyExistsError(ApplicationError):
    user_id: UUID


@dataclass(eq=False)
class UserIdNotExistError(ApplicationError):
    user_id: UUID


@dataclass(eq=False)
class UsernameNotExistError(ApplicationError):
    username: str
