from datetime import datetime

from pydantic import BaseModel
from pydantic import Field
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text


class PostBase(BaseModel):
    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)


class PostPartialUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class PostCreate(PostBase):
    pass


class PostDB(PostBase):
    id: int


metadata = MetaData()


posts = Table(
    "posts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("publication_date", DateTime, nullable=False),
    Column("title", String(length=255), nullable=False),
    Column("content", Text, nullable=False),
)
