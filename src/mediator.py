from dataclasses import dataclass
from typing import Any

from app.common.commands import Command, CommandDispatcher, CommandDispatcherImpl, CommandHandler, CRes
from app.users.commands import CreateUser, CreateUserHandler


@dataclass
class Mediator:
    command_dispatcher: CommandDispatcher

    async def handle_command(self, command: Command[CRes], *args: Any, **kwargs: Any) -> CRes:
        return await self.command_dispatcher.send(command, *args, **kwargs)

    def register_command_handler(self, command: type[Command], handler: type[CommandHandler[Command, CRes]]) -> None:
        self.command_dispatcher.register_handler(command, handler)


def init_mediator() -> Mediator:
    return Mediator(command_dispatcher=CommandDispatcherImpl())


def setup_mediator(mediator: Mediator) -> None:
    mediator.register_command_handler(command=CreateUser, handler=CreateUserHandler)
