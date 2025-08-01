from typing import NoReturn

from app.common.exceptions import RepositoryError
from app.users.exceptions import UserIdAlreadyExistsError
from domain.users import entities
from domain.users.exeptions import UsernameAlreadyExistsError
from domain.users.repositories import UserRepository
from domain.users.value_objects import UserId, Username
from infra.db.models.users import UserModel
from infra.db.repositories.base import SQLAlchemyRepository
from sqlalchemy import exists, select
from sqlalchemy.exc import DBAPIError, IntegrityError


class UserRepositoryImpl(SQLAlchemyRepository, UserRepository):
    async def get_user_by_id(self, user_id: UserId) -> entities.User | None:
        return await self.session.get(entities.User, user_id.to_representative())

    async def check_username_exists(self, username: Username) -> bool:
        result = await self.session.scalar(select(exists().where(UserModel.username == username.to_representative())))
        return bool(result)

    async def create_user(self, user: entities.User) -> None:
        self.session.add(user)
        try:
            await self.session.flush()
        except IntegrityError as exc:
            self._parse_exception(exc, user)

    def _parse_exception(self, exc: DBAPIError, user: entities.User) -> NoReturn:
        match exc.__cause__.__cause__.constraint_name:
            case "pk_users":
                raise UserIdAlreadyExistsError(user.id.to_representative()) from exc
            case "uq_users_username":
                raise UsernameAlreadyExistsError(str(user.username)) from exc
            case _:
                raise RepositoryError from exc
