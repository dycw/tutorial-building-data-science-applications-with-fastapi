from asyncio import AbstractEventLoop
from asyncio import get_event_loop
from collections.abc import Iterator

from fastapi.testclient import TestClient
from pytest import fixture
from pytest import mark

from app.chapter09.websocket import app


@fixture(scope="session")
def event_loop() -> Iterator[AbstractEventLoop]:
    loop = get_event_loop()
    yield loop
    loop.close()


@fixture
def websocket_client() -> Iterator[TestClient]:
    with TestClient(app) as websocket_client:
        yield websocket_client


@mark.asyncio
async def test_websocket_echo(websocket_client: TestClient) -> None:
    with websocket_client.websocket_connect("/ws") as websocket:
        websocket.send_text("Hello")
        message = websocket.receive_text()
        assert message == "Message text was: Hello"
