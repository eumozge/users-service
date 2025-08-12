from fastapi import status
from httpx import AsyncClient
from tests.api.fixtures import Resolver


async def test(resolver: Resolver, client: AsyncClient) -> None:
    url = resolver("healthcheck")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
