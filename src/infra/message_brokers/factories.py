import aio_pika
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool
from infra.message_brokers.exceptions import MessageBrokerError
from settings import MessageBrokerSettings


class ConnectionFactory:
    def __init__(self, settings: MessageBrokerSettings) -> None:
        self._settings = settings

    async def get_connection(self) -> AbstractRobustConnection:
        return await aio_pika.connect_robust(
            host=self._settings.host,
            port=self._settings.port,
            login=self._settings.login,
            password=self._settings.password,
        )


class ChannelFactory:
    def __init__(self, rq_connection_pool: Pool[aio_pika.abc.AbstractConnection]) -> None:
        self._rq_connection_pool = rq_connection_pool

    async def get_channel(self) -> aio_pika.abc.AbstractChannel:
        async with self._rq_connection_pool.acquire() as connection:
            try:
                return await connection.channel()
            except Exception as exc:
                raise MessageBrokerError from exc
