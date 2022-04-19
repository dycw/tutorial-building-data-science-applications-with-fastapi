from collections.abc import Mapping
from typing import Any
from typing import cast

from databases import Database
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Query
from fastapi import status

from app.chapter6.sqlalchemy_relationship.database import get_database
from app.chapter6.sqlalchemy_relationship.database import sqlalchemy_engine
from app.chapter6.sqlalchemy_relationship.models import CommentCreate
from app.chapter6.sqlalchemy_relationship.models import CommentDB
from app.chapter6.sqlalchemy_relationship.models import PostCreate
from app.chapter6.sqlalchemy_relationship.models import PostDB
from app.chapter6.sqlalchemy_relationship.models import PostPartialUpdate
from app.chapter6.sqlalchemy_relationship.models import PostPublic
from app.chapter6.sqlalchemy_relationship.models import comments
from app.chapter6.sqlalchemy_relationship.models import metadata
from app.chapter6.sqlalchemy_relationship.models import posts


app = FastAPI()


@app.on_event("startup")  # type: ignore
async def startup() -> None:
    await get_database().connect()
    metadata.create_all(sqlalchemy_engine)


@app.on_event("shutdown")  # type: ignore
async def shutdown() -> None:
    await get_database().disconnect()


async def pagination(
    skip: int = Query(0, ge=0), limit: int = Query(10, ge=0)
) -> tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)


async def get_post_or_404(
    id: int, database: Database = Depends(get_database)
) -> PostPublic:
    select_post_query = posts.select().where(posts.c.id == id)
    if (raw_post := await database.fetch_one(select_post_query)) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    select_post_comments_query = comments.select().where(
        comments.c.post_id == id
    )
    raw_comments = await database.fetch_all(select_post_comments_query)
    comments_list = [CommentDB(**comment) for comment in raw_comments]
    return PostPublic(**raw_post, comments=comments_list)


@app.get("/posts")
async def list_posts(
    pagination: tuple[int, int] = Depends(pagination),
    database: Database = Depends(get_database),
) -> list[PostDB]:
    skip, limit = pagination
    select_query = posts.select().offset(skip).limit(limit)
    rows = await database.fetch_all(select_query)
    return [PostDB(**row) for row in rows]


@app.get("/posts/{id}", response_model=PostPublic)
async def get_post(post: PostPublic = Depends(get_post_or_404)) -> PostPublic:
    return post


@app.post(
    "/posts", response_model=PostPublic, status_code=status.HTTP_201_CREATED
)
async def create_post(
    post: PostCreate, database: Database = Depends(get_database)
) -> PostPublic:
    insert_query = posts.insert().values(post.dict())
    post_id = await database.execute(insert_query)
    return await get_post_or_404(post_id, database)


@app.patch("/posts/{id}", response_model=PostPublic)
async def update_post(
    post_update: PostPartialUpdate,
    post: PostPublic = Depends(get_post_or_404),
    database: Database = Depends(get_database),
) -> PostPublic:
    update_query = (
        posts.update()
        .where(posts.c.id == post.id)
        .values(post_update.dict(exclude_unset=True))
    )
    post_id = await database.execute(update_query)
    return await get_post_or_404(post_id, database)


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post: PostPublic = Depends(get_post_or_404),
    database: Database = Depends(get_database),
) -> None:
    delete_query = posts.delete().where(posts.c.id == post.id)
    await database.execute(delete_query)


@app.post(
    "/comments", response_model=CommentDB, status_code=status.HTTP_201_CREATED
)
async def create_comment(
    comment: CommentCreate, database: Database = Depends(get_database)
) -> CommentDB:
    select_post_query = posts.select().where(posts.c.id == comment.post_id)
    if (await database.fetch_one(select_post_query)) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Post {id} does not exist",
        )
    insert_query = comments.insert().values(comment.dict())
    comment_id = await database.execute(insert_query)
    select_query = comments.select().where(comments.c.id == comment_id)
    raw_comment = cast(
        Mapping[str, Any], await database.fetch_one(select_query)
    )
    return CommentDB(**raw_comment)
