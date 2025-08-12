from fastapi import status
from httpx import AsyncClient
from tests.api.fixtures import Resolver


async def test_create_user(resolver: Resolver, client: AsyncClient) -> None:
    url = resolver("create_user")
    response = await client.post(url, json={"username": "username"})
    assert response.status_code == status.HTTP_201_CREATED
