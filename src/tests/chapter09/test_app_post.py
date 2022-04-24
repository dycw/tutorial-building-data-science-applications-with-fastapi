from asyncio import AbstractEventLoop
from asyncio import get_event_loop
from collections.abc import AsyncIterator
from collections.abc import Iterator

from asgi_lifespan import LifespanManager
from fastapi import status
from httpx import AsyncClient
from pytest import fixture
from pytest import mark

from app.chapter09.app_post import app


@fixture(scope="session")
def event_loop() -> Iterator[AbstractEventLoop]:
    loop = get_event_loop()
    yield loop
    loop.close()


@fixture
async def test_client() -> AsyncIterator[AsyncClient]:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app, base_url="http://app.io"
        ) as test_client:
            yield test_client


@mark.asyncio
class TestCreatePerson:
    async def test_invalid(self, test_client: AsyncClient) -> None:
        payload = {"first_name": "John", "last_name": "Doe"}
        response = await test_client.post("/persons", json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid(self, test_client: AsyncClient) -> None:
        payload = {"first_name": "John", "last_name": "Doe", "age": 30}
        response = await test_client.post("/persons", json=payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == payload
