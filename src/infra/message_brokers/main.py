from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import aio_pika
from aio_pika.pool import Pool
from infra.message_brokers.factories import ChannelFactory, ConnectionFactory
from settings import MessageBrokerSettings


@asynccontextmanager
async def build_connnection_pool(
    settings: MessageBrokerSettings,
) -> AsyncGenerator[Pool[aio_pika.abc.AbstractConnection], None]:
    factory = ConnectionFactory(settings)
    connection_pool = Pool(factory.get_connection, max_size=10)
    async with connection_pool:
        yield connection_pool


@asynccontextmanager
async def build_channel_pool(
    connection_pool: Pool[aio_pika.abc.AbstractConnection],
) -> AsyncGenerator[Pool[aio_pika.abc.AbstractChannel], None]:
    factory = ChannelFactory(connection_pool)
    pool = Pool(factory.get_channel, max_size=100)
    async with pool:
        yield pool
