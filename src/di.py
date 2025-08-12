from dependency_injector import containers, providers
from infra.db.main import get_sa_session_maker
from sqlalchemy.ext.asyncio import AsyncEngine


class DIContainer(containers.DeclarativeContainer):
    db_engine = providers.Provider()
    db_session_maker = providers.Factory(get_sa_session_maker, engine=db_engine)


def get_container(db_engine: AsyncEngine) -> DIContainer:
    container = DIContainer()
    container.db_engine.override(providers.Object(db_engine))
    container.init_resources()
    return container
