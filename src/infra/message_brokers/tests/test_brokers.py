from collections.abc import AsyncGenerator
from typing import Any

import aio_pika
import orjson
import pytest
from infra.message_brokers.brokers import MessageBrokerImpl
from infra.message_brokers.main import build_channel_pool, build_connnection_pool
from infra.message_brokers.messages import Message
from settings import settings


class TestMessageBrokerImpl:
    @pytest.fixture()
    async def channel(self) -> AsyncGenerator[aio_pika.abc.AbstractChannel, Any]:
        async with (
            build_connnection_pool(settings.message_broker) as connection,
            build_channel_pool(connection) as channel_pool,
            channel_pool.acquire() as channel,
        ):
            yield channel

    async def test_publish_message(self, channel: aio_pika.abc.AbstractChannel) -> None:
        reference_message = Message(data="some payload")

        message_broker = MessageBrokerImpl(channel)
        await message_broker.declare_exchange("tests")
        await message_broker.publish_message(message=reference_message, routing_key="tests", exchange_name="tests")

        queue: aio_pika.abc.AbstractQueue = await channel.declare_queue("tests")
        queue = await channel.declare_queue(
            "tests",
        )
        message = await queue.get(timeout=1)
        body = orjson.loads(message.body.decode())
        assert reference_message.data == body["data"]
