from dependency_injector import containers, providers
from domain.users.services import UserService
from infra.db.main import get_sa_session_maker
from infra.db.repositories.users import UserRepositoryImpl
from infra.db.uow import SQLAlchemyUoW
from sqlalchemy.ext.asyncio import AsyncEngine


class DI(containers.DeclarativeContainer):
    db_engine = providers.Provider()
    db_session_maker = providers.Factory(get_sa_session_maker, engine=db_engine)

    db_uow = providers.Factory(SQLAlchemyUoW)
    user_repository = providers.Factory(UserRepositoryImpl)
    user_service = providers.Factory(UserService)


def get_container(db_engine: AsyncEngine) -> DI:
    container = DI()
    container.db_engine.override(providers.Object(db_engine))
    container.init_resources()
    return container
