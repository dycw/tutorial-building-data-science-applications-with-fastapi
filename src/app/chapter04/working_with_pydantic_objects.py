from dataclasses import dataclass
from dataclasses import field
from datetime import date
from enum import Enum
from enum import auto
from typing import Any
from typing import Optional
from typing import cast

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from pydantic import BaseModel


class Gender(str, Enum):
    def _generate_next_value_(name, *_: Any) -> str:  # type: ignore
        return name

    MALE = auto()
    FEMALE = auto()
    NON_BINARY = auto()


class Address(BaseModel):
    street_address: str
    postal_code: str
    city: str
    country: str


class Person(BaseModel):
    first_name: str
    last_name: str
    gender: Gender
    birthdate: date
    interests: list[str]
    address: Address

    def name_dict(self) -> dict[str, Any]:
        return self.dict(include={"first_name", "last_name"})


class PostBase(BaseModel):
    title: str
    content: str

    def excerpt(self) -> str:
        return f"{self.content[:140]}..."


class PostCreate(PostBase):
    pass


class PostPublic(PostBase):
    id: int


class PostDB(PostBase):
    id: int
    nb_views: int = 0


@dataclass
class DummyDatabase:
    posts: dict[int, PostDB] = field(default_factory=dict)


db = DummyDatabase()
app = FastAPI()


@app.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=PostPublic
)
async def create(post_create: PostCreate) -> PostPublic:
    new_id = max(db.posts.keys(), default=0) + 1
    post = PostDB(id=new_id, **post_create.dict())
    db.posts[new_id] = post
    return cast(PostPublic, post)


class PostPartialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


@app.patch("/posts/{id}", response_model=PostPublic)
async def partial_update(id: int, post_update: PostPartialUpdate) -> PostPublic:
    try:
        post_db = db.posts[id]
    except KeyError:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    else:
        updated_fields = post_update.dict(exclude_unset=True)
        updated_post = post_db.copy(update=updated_fields)
        db.posts[id] = updated_post
        return cast(PostPublic, updated_post)
