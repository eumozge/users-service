from collections.abc import AsyncGenerator, Callable
from typing import Any

import pytest
from api.main import init
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

Resolver = Callable[[str], str]


@pytest.fixture()
def app() -> FastAPI:
    return init()


@pytest.fixture()
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        yield async_client


@pytest.fixture()
async def resolver(app: FastAPI) -> Resolver:
    def inner(name: str, **kwargs: Any) -> str:
        return app.url_path_for(name, **kwargs)

    return inner
