from databases import Database
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Query
from fastapi import status

from app.chapter06.sqlalchemy.database import get_database
from app.chapter06.sqlalchemy.database import sqlalchemy_engine
from app.chapter06.sqlalchemy.models import PostCreate
from app.chapter06.sqlalchemy.models import PostDB
from app.chapter06.sqlalchemy.models import PostPartialUpdate
from app.chapter06.sqlalchemy.models import metadata
from app.chapter06.sqlalchemy.models import posts


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
    return skip, capped_limit


async def get_post_or_404(
    id: int, database: Database = Depends(get_database)
) -> PostDB:
    select_query = posts.select().where(posts.c.id == id)
    if (raw_post := await database.fetch_one(select_query)) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return PostDB(**raw_post)


@app.get("/posts")
async def list_posts(
    pagination: tuple[int, int] = Depends(pagination),
    database: Database = Depends(get_database),
) -> list[PostDB]:
    skip, limit = pagination
    select_query = posts.select().offset(skip).limit(limit)
    rows = await database.fetch_all(select_query)
    return [PostDB(**row) for row in rows]


@app.get("/posts/{id}", response_model=PostDB)
async def get_post(post: PostDB = Depends(get_post_or_404)) -> PostDB:
    return post


@app.post("/posts", response_model=PostDB, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate, database: Database = Depends(get_database)
) -> PostDB:
    insert_query = posts.insert().values(post.dict())
    post_id = await database.execute(insert_query)
    return await get_post_or_404(post_id, database)


@app.patch("/posts/{id}", response_model=PostDB)
async def update_post(
    post_update: PostPartialUpdate,
    post: PostDB = Depends(get_post_or_404),
    database: Database = Depends(get_database),
) -> PostDB:
    update_query = (
        posts.update()
        .where(posts.c.id == post.id)
        .values(post_update.dict(exclude_unset=True))
    )
    post_id = await database.execute(update_query)
    return await get_post_or_404(post_id, database)


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post: PostDB = Depends(get_post_or_404),
    database: Database = Depends(get_database),
) -> None:
    delete_query = posts.delete().where(posts.c.id == post.id)
    await database.execute(delete_query)
