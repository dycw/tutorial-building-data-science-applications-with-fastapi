from datetime import datetime
from typing import Any
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import validator
from tortoise.fields import CharField
from tortoise.fields import DatetimeField
from tortoise.fields import ForeignKeyField
from tortoise.fields import IntField
from tortoise.fields import TextField
from tortoise.models import Model


class CommentBase(BaseModel):
    post_id: int
    publication_date: datetime = Field(default_factory=datetime.now)
    content: str

    class Config:
        orm_mode = True


class CommentCreate(CommentBase):
    pass


class CommentDB(CommentBase):
    id: int


class PostBase(BaseModel):
    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class PostPartialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostDB(PostBase):
    id: int


class PostPublic(PostDB):
    comments: list[CommentDB]

    @validator("comments", pre=True)
    def fetch_comments(cls, v: Any) -> list[Any]:  # noqa: U100
        return list(v)


class CommentTortoise(Model):
    id = IntField(pk=True, generated=True)
    post = ForeignKeyField(
        "models.PostTortoise", related_name="comments", null=False
    )
    publication_date = DatetimeField(null=False)

    content = TextField(null=False)

    class Meta:  # type: ignore
        table = "comments"


class PostTortoise(Model):
    id = IntField(pk=True, generated=True)
    publication_date = DatetimeField(null=False)
    title = CharField(max_length=255, null=False)
    content = TextField(null=False)

    class Meta:  # type: ignore
        table = "posts"
