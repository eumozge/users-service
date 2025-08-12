from dataclasses import dataclass

from app.common.exceptions import CommitError, RollbackError
from app.common.interfaces import UnitOfWork
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass(eq=False)
class SQLAlchemyUoW(UnitOfWork):
    session: AsyncSession

    async def commit(self) -> None:
        try:
            await self.session.commit()
        except SQLAlchemyError as err:
            raise CommitError from err

    async def rollback(self) -> None:
        try:
            await self.session.rollback()
        except SQLAlchemyError as err:
            raise RollbackError from err
