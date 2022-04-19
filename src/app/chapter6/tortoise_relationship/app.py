from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Query
from fastapi import status
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist

from app.chapter6.tortoise_relationship.models import CommentBase
from app.chapter6.tortoise_relationship.models import CommentDB
from app.chapter6.tortoise_relationship.models import CommentTortoise
from app.chapter6.tortoise_relationship.models import PostCreate
from app.chapter6.tortoise_relationship.models import PostDB
from app.chapter6.tortoise_relationship.models import PostPartialUpdate
from app.chapter6.tortoise_relationship.models import PostTortoise


app = FastAPI()


async def pagination(
    skip: int = Query(0, ge=0), limit: int = Query(10, ge=0)
) -> tuple[int, int]:
    capped_limit = min(100, limit)
    return skip, capped_limit


async def get_post_or_404(id: int) -> PostTortoise:
    try:
        return await PostTortoise.get(id=id).prefetch_related(  # type: ignore
            "comments"
        )
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/posts")
async def list_post(
    pagination: tuple[int, int] = Depends(pagination)
) -> list[PostDB]:
    skip, limit = pagination
    posts = await PostTortoise.all().offset(skip).limit(limit)
    return [PostDB.from_orm(post) for post in posts]


@app.get("/posts/{id}", response_model=PostDB)
async def get_post(post: PostTortoise = Depends(get_post_or_404)) -> PostDB:
    return PostDB.from_orm(post)


@app.post("/posts", response_model=PostDB, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate) -> PostDB:
    post_tortoise = await PostTortoise.create(**post.dict())
    return PostDB.from_orm(post_tortoise)


@app.patch("/posts/{id}", response_model=PostDB)
async def update_post(
    post_update: PostPartialUpdate,
    post: PostTortoise = Depends(get_post_or_404),
) -> PostDB:
    _ = post.update_from_dict(post_update.dict(exclude_unset=True))
    await post.save()
    return PostDB.from_orm(post)


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post: PostTortoise = Depends(get_post_or_404)) -> None:
    await post.delete()


@app.post("/comments", response_model=CommentDB)
async def create_comment(comment: CommentBase) -> CommentDB:
    try:
        _ = await PostTortoise.get(id=comment.post_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Post {id} does not exist",
        )
    else:
        comment_tortoise = await CommentTortoise.create(**comment.dict())
        return CommentDB.from_orm(comment_tortoise)


TORTOISE_ORM = {
    "connections": {"default": "sqlite://chapter6_tortoise.db"},
    "apps": {
        "models": {
            "models": ["app.chapter6.tortoise_relationship.models"],
            "default_connection": "default",
        }
    },
}

register_tortoise(
    app, config=TORTOISE_ORM, generate_schemas=True, add_exception_handlers=True
)
