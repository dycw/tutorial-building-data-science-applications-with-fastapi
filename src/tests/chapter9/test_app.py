from asyncio import AbstractEventLoop
from asyncio import get_event_loop
from collections.abc import AsyncIterator
from collections.abc import Iterator

from asgi_lifespan import LifespanManager
from fastapi import status
from httpx import AsyncClient
from pytest import fixture
from pytest import mark

from app.chapter9.app import app


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
async def test_hello_world(test_client: AsyncClient) -> None:
    response = await test_client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"hello": "world"}
