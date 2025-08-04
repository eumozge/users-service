import aio_pika
from aiormq import AMQPError
from app.common.exceptions import CommitError, RollbackError
from app.common.interfaces import UnitOfWork


class RabbitMQUoW(UnitOfWork):
    def __init__(self, rq_transaction: aio_pika.abc.AbstractTransaction) -> None:
        self._rq_transaction = rq_transaction

    async def commit(self) -> None:
        try:
            await self._rq_transaction.commit()
        except AMQPError as err:
            raise CommitError from err

    async def rollback(self) -> None:
        try:
            await self._rq_transaction.rollback()
        except AMQPError as err:
            raise RollbackError from err
