from fastapi import status
from httpx import AsyncClient
from presentation.api.tests.fixtures import Resolver


async def test(resolver: Resolver, client: AsyncClient) -> None:
    url = resolver("healthcheck")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
