from abc import ABC, abstractmethod
from mailbox import Message


class MessageBroker(ABC):
    @abstractmethod
    async def publish_message(self, message: Message, routing_key: str, exchange_name: str) -> None: ...

    @abstractmethod
    async def declare_exchange(self, exchange_name: str) -> None: ...
