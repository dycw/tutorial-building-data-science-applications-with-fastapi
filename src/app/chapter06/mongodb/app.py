from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Query
from fastapi import status
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.chapter06.mongodb.models import PostCreate
from app.chapter06.mongodb.models import PostDB
from app.chapter06.mongodb.models import PostPartialUpdate


app = FastAPI()
motor_client = AsyncIOMotorClient("mongodb://localhost:27017")  # whole server
database = motor_client["chapter06_mongo"]  # single database instance


def get_database() -> AsyncIOMotorDatabase:
    return database


async def pagination(
    skip: int = Query(0, ge=0), limit: int = Query(10, ge=0)
) -> tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)


async def get_object_id(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


async def get_post_or_404(
    id: ObjectId = Depends(get_object_id),
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> PostDB:
    if (raw_post := await database["posts"].find_one({"_id": id})) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return PostDB(**raw_post)


@app.get("/posts")
async def list_posts(
    pagination: tuple[int, int] = Depends(pagination),
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> list[PostDB]:
    skip, limit = pagination
    query = database["posts"].find({}, skip=skip, limit=limit)
    return [PostDB(**raw_post) async for raw_post in query]


@app.get("/posts/{id}", response_model=PostDB)
async def get_post(post: PostDB = Depends(get_post_or_404)) -> PostDB:
    return post


@app.post("/posts", response_model=PostDB, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate, database: AsyncIOMotorDatabase = Depends(get_database)
) -> PostDB:
    post_db = PostDB(**post.dict())
    await database["posts"].insert_one(post_db.dict(by_alias=True))
    return await get_post_or_404(post_db.id, database)


@app.patch("/posts/{id}", response_model=PostDB)
async def update_post(
    post_update: PostPartialUpdate,
    post: PostDB = Depends(get_post_or_404),
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> PostDB:
    await database["posts"].update_one(
        {"_id": post.id}, {"$set": post_update.dict(exclude_unset=True)}
    )
    return await get_post_or_404(post.id, database)


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post: PostDB = Depends(get_post_or_404),
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> None:
    await database["posts"].delete_one({"_id": post.id})
