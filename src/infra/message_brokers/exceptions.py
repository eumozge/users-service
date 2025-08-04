from dataclasses import dataclass

from app.common.exceptions import ApplicationError


@dataclass(eq=False)
class MessageBrokerError(ApplicationError):
    pass
