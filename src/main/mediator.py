from dataclasses import dataclass

from app.common.commands import Command, CommandDispatcher, CommandHandler, CRes


@dataclass
class Mediator:
    command_dispatcher: CommandDispatcher

    async def send(self, command: Command[CRes]) -> CRes:
        return await self.command_dispatcher.send(command)

    def register_command_handler(self, command: type[Command], handler: CommandHandler[Command, CRes]) -> None:
        self.command_dispatcher.register_handler(command, handler)
