from typing import cast

from fastapi import FastAPI
from fastapi import status
from pydantic import BaseModel


class Post1(BaseModel):
    title: str


app = FastAPI()


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post1) -> Post1:
    return post


class Post2(BaseModel):
    title: str
    nb_views: int


posts = {1: Post2(title="Hello", nb_views=100)}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int) -> None:
    del posts[id]


@app.get("/posts-1/{id}")
async def get_post_1(id: int) -> Post2:
    return posts[id]


@app.get("/posts-2/{id}", response_model=Post1)
async def get_post_2(id: int) -> Post1:
    return cast(Post1, posts[id])
