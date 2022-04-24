from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text


class CommentBase(BaseModel):
    post_id: int
    publication_date: datetime = Field(default_factory=datetime.now)
    content: str


class CommentCreate(CommentBase):
    pass


class CommentDB(CommentBase):
    id: int


class PostBase(BaseModel):
    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)


class PostPartialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostDB(PostBase):
    id: int


class PostPublic(PostDB):
    comments: list[CommentDB]


metadata = MetaData()


posts = Table(
    "posts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("publication_date", DateTime(), nullable=False),
    Column("title", String(length=255), nullable=False),
    Column("content", Text, nullable=False),
)

comments = Table(
    "comments",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "post_id", ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    ),
    Column("publication_date", DateTime, nullable=False),
    Column("content", Text, nullable=False),
)
