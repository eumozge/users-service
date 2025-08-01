from dataclasses import dataclass
from uuid import UUID

from app.common.dto import DTO


@dataclass(frozen=True)
class User(DTO):
    id: UUID
    username: str
