from asyncio import AbstractEventLoop
from asyncio import get_event_loop
from collections.abc import AsyncIterator
from collections.abc import Iterator
from typing import Any

from asgi_lifespan import LifespanManager
from fastapi import status
from httpx import AsyncClient
from pytest import fixture
from pytest import mark

from app.chapter09.app_external_api import app
from app.chapter09.app_external_api import external_api


class MockExternalAPI:
    mock_data = {
        "data": [
            {
                "employee_age": 61,
                "employee_name": "Tiger Nixon",
                "employee_salary": 320800,
                "id": 1,
                "profile_image": "",
            }
        ],
        "status": "success",
        "message": "Success",
    }

    async def __call__(self) -> dict[str, Any]:
        return MockExternalAPI.mock_data


@fixture(scope="session")
def event_loop() -> Iterator[AbstractEventLoop]:
    loop = get_event_loop()
    yield loop
    loop.close()


@fixture
async def test_client() -> AsyncIterator[AsyncClient]:
    app.dependency_overrides[external_api] = MockExternalAPI()
    async with LifespanManager(app):
        async with AsyncClient(
            app=app, base_url="http://app.io"
        ) as test_client:
            yield test_client


@mark.asyncio
async def test_get_employees(test_client: AsyncClient) -> None:
    response = await test_client.get("/employees")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == MockExternalAPI.mock_data
