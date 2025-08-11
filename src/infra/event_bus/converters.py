from app.common.exceptions import MappingError
from domain.common.events import Event
from domain.users.events import UserCreated
from infra.event_bus import events as integration_events


def convert_user_created_to_integration(
    event: UserCreated,
) -> integration_events.UserCreated:
    return integration_events.UserCreated(
        user_id=event.user_id,
        username=event.username,
    )


def convert_domain_event_to_integration(
    event: Event,
) -> integration_events.IntegrationEvent:
    if isinstance(event, UserCreated):
        return convert_user_created_to_integration(event)
    raise MappingError(event)
