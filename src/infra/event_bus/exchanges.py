from infra.message_broker.interfaces import MessageBroker

USERS_EXCHANGE = "users"


async def declare_exchanges(message_broker: MessageBroker) -> None:
    await message_broker.declare_exchange(USERS_EXCHANGE)
