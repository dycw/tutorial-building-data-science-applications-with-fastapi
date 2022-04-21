from dataclasses import dataclass
from dataclasses import field
from typing import Any

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Query
from pydantic import BaseModel
from starlette import status


app = FastAPI()


async def pagination_1(skip: int = 0, limit: int = 10) -> tuple[int, int]:
    return skip, limit


@app.get("/items")
async def list_items(
    p: tuple[int, int] = Depends(pagination_1)
) -> dict[str, Any]:
    skip, limit = p
    return {"skip": skip, "limit": limit}


@app.get("/things")
async def list_things(
    p: tuple[int, int] = Depends(pagination_1)
) -> dict[str, Any]:
    skip, limit = p
    return {"skip": skip, "limit": limit}


async def pagination_2(
    skip: int = Query(0, ge=0), limit: int = Query(10, ge=0)
) -> tuple[int, int]:
    capped_limit = min(100, limit)
    return skip, capped_limit


class Post(BaseModel):
    id: int
    title: str
    content: str


class PostUpdate(BaseModel):
    title: str | None
    content: str | None


@dataclass
class DummyDatabase:
    posts: dict[int, Post] = field(default_factory=dict)


db = DummyDatabase()
db.posts = {
    1: Post(id=1, title="Post 1", content="Content 1"),
    2: Post(id=2, title="Post 2", content="Content 2"),
    3: Post(id=3, title="Post 3", content="Content 3"),
}


async def get_post_or_404(id: int) -> Post:
    try:
        return db.posts[id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/posts/{id}")
async def get(post: Post = Depends(get_post_or_404)) -> Post:
    return post


@app.patch("/posts/{id}")
async def update(
    post_update: PostUpdate, post: Post = Depends(get_post_or_404)
) -> Post:
    updated_post = post.copy(update=post_update.dict())
    db.posts[post.id] = updated_post
    return updated_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(post: Post = Depends(get_post_or_404)) -> None:
    _ = db.posts.pop(post.id)
