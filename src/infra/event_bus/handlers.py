from typing import Any

from app.common.events import EventHandler
from domain.common.events import Event
from infra.event_bus.bus import EventBusImpl
from infra.event_bus.converters import convert_domain_event_to_integration


class EventHandlerPublisher(EventHandler[Event]):
    def __init__(self, event_bus: EventBusImpl) -> None:
        self.event_bus = event_bus

    async def __call__(self, event: Event) -> Any:
        integration_event = convert_domain_event_to_integration(event)
        await self.event_bus.publish_event(integration_event)
