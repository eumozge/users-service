from api.tests.fixtures import Resolver
from fastapi import status
from httpx import AsyncClient


async def test(resolver: Resolver, client: AsyncClient) -> None:
    url = resolver("healthcheck")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
