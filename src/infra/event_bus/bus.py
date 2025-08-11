import logging

import orjson
from infra.event_bus.events import IntegrationEvent
from infra.message_broker.interfaces import MessageBroker
from infra.message_broker.messages import Message

logger = logging.getLogger(__name__)


class EventBusImpl:
    def __init__(self, message_broker: MessageBroker) -> None:
        self.message_broker = message_broker

    async def publish_event(self, event: IntegrationEvent) -> None:
        message = self.build_message(event)
        await self.message_broker.publish_message(
            message=message,
            routing_key=event.routing_key,
            exchange_name=event.exchange_name,
        )
        logger.debug("Event published", extra={"event": event})

    def build_message(self, event: IntegrationEvent) -> Message:
        return Message(id=event.event_id, data=orjson.dumps(event).decode(), message_type="event")
