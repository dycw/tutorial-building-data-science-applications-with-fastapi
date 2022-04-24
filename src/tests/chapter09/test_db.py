from asyncio import AbstractEventLoop
from asyncio import get_event_loop
from collections.abc import AsyncIterator
from collections.abc import Iterator
from typing import Any

from asgi_lifespan import LifespanManager
from bson import ObjectId
from fastapi import status
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from pytest import fixture
from pytest import mark

from app.chapter06.mongodb.app import app
from app.chapter06.mongodb.app import get_database
from app.chapter06.mongodb.models import PostDB


motor_client = AsyncIOMotorClient("mongodb://localhost:27017")
database_test = motor_client["chapter09_db_test"]


def get_test_database() -> Any:
    return database_test


@fixture(scope="session")
def event_loop() -> Iterator[AbstractEventLoop]:
    loop = get_event_loop()
    yield loop
    loop.close()


@fixture
async def test_client() -> AsyncIterator[AsyncClient]:
    app.dependency_overrides[get_database] = get_test_database
    async with LifespanManager(app):
        async with AsyncClient(
            app=app, base_url="http://app.io"
        ) as test_client:
            yield test_client


@fixture(autouse=True, scope="module")
async def initial_posts() -> AsyncIterator[list[PostDB]]:
    initial_posts = [
        PostDB(title="Post 1", content="Content 1"),
        PostDB(title="Post 2", content="Content 2"),
        PostDB(title="Post 3", content="Content 3"),
    ]
    await database_test["posts"].insert_many(
        [post.dict(by_alias=True) for post in initial_posts]
    )
    yield initial_posts
    await motor_client.drop_database("chapter09_db_test")


@mark.asyncio
@mark.skip(reason="mongo db missing")
class TestGetPost:
    async def test_not_existing(self, test_client: AsyncClient) -> None:
        response = await test_client.get("/posts/abc")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_existing(
        self, test_client: AsyncClient, initial_posts: list[PostDB]
    ) -> None:
        response = await test_client.get(f"/posts/{initial_posts[0].id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["_id"] == str(initial_posts[0].id)


@mark.asyncio
@mark.skip(reason="mongo db missing")
class TestCreatePost:
    async def test_invalid_payload(self, test_client: AsyncClient) -> None:
        payload = {"title": "New post"}
        response = await test_client.post("/posts", json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid_payload(self, test_client: AsyncClient) -> None:
        payload = {"title": "New post", "content": "New post content"}
        response = await test_client.post("/posts", json=payload)
        assert response.status_code == status.HTTP_201_CREATED
        post_id = ObjectId(response.json()["_id"])
        post_db = await database_test["posts"].find_one({"_id": post_id})
        assert post_db is not None
