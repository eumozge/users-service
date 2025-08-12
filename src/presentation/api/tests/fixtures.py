from collections.abc import AsyncGenerator, Callable
from typing import Any

import pytest
from di import DIContainer, get_container
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from mediator import init_mediator, setup_mediator
from presentation.api.main import init_api
from sqlalchemy.ext.asyncio import AsyncEngine

Resolver = Callable[[str], str]


@pytest.fixture()
async def di(db_engine: AsyncEngine) -> DIContainer:
    return get_container(db_engine)


@pytest.fixture()
def app(di: DIContainer) -> FastAPI:
    mediator = init_mediator(di=di)
    setup_mediator(mediator)
    return init_api(mediator=mediator)


@pytest.fixture()
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        yield async_client


@pytest.fixture()
async def resolver(app: FastAPI) -> Resolver:
    def inner(name: str, **kwargs: Any) -> str:
        return app.url_path_for(name, **kwargs)

    return inner
