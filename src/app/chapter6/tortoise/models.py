from datetime import datetime

from pydantic import BaseModel
from pydantic import Field
from tortoise.fields import CharField
from tortoise.fields import DatetimeField
from tortoise.fields import IntField
from tortoise.fields import TextField
from tortoise.models import Model


class PostBase(BaseModel):
    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class PostPartialUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class PostCreate(PostBase):
    pass


class PostDB(PostBase):
    id: int


class PostTortoise(Model):
    id = IntField(pk=True, generated=True)
    publication_date = DatetimeField(null=False)
    title = CharField(max_length=255, null=False)
    content = TextField(null=False)

    class Meta:  # type: ignore
        table = "posts"
