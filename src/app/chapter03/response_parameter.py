from typing import Any

from fastapi import FastAPI
from fastapi import Response
from fastapi import status
from pydantic import BaseModel


app = FastAPI()


@app.get("/1")
async def custom_header(response: Response) -> dict[str, Any]:
    response.headers["Custom-Header"] = "Custom-Header-Value"
    return {"hello": "world"}


@app.get("/2")
async def custom_cookie(response: Response) -> dict[str, Any]:
    response.set_cookie("cookie-name", "cookie-value", max_age=86400)
    return {"hello": "world"}


class Post(BaseModel):
    title: str


posts = {1: Post(title="Hello")}


@app.put("/posts/{id}")
async def update_or_create_post(
    id: int, post: Post, response: Response
) -> Post:
    if id not in posts:
        response.status_code = status.HTTP_201_CREATED
    posts[id] = post
    return posts[id]
