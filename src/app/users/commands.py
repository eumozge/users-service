import logging
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from app.common.commands import Command, CommandHandler
from app.common.interfaces import UnitOfWork
from domain.users.services import UserService
from domain.users.value_objects import UserId, Username

logger = logging.getLogger(__name__)


@dataclass(eq=False, frozen=True, kw_only=True)
class CreateUser(Command):
    user_id: UUID = field(default_factory=uuid4)
    username: str


class CreateUserHandler(CommandHandler[CreateUser, UUID]):
    def __init__(self, user_service: UserService, uow: UnitOfWork) -> None:
        self.user_service = user_service
        self.uow = uow

    async def __call__(self, command: CreateUser) -> UUID:
        """TODO Add publishing of users event."""
        user_id = UserId(command.user_id)
        username = Username(command.username)
        user = await self.user_service.create_user(user_id=user_id, username=username)
        await self.uow.commit()

        logger.info("User craeted", extra={"user_id": user_id.to_representative(), "user": user})

        return user.id.to_representative()
