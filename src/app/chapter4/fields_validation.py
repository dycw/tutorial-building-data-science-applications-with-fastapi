from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class Person(BaseModel):
    first_name: str = Field(..., min_length=3)
    last_name: str = Field(..., min_length=3)
    age: int | None = Field(None, ge=0, le=120)


def list_factory() -> list[str]:
    return ["a", "b", "c"]


class Model(BaseModel):
    l: list[str] = Field(default_factory=list_factory)
    d: datetime = Field(default_factory=datetime.now)
    l2: list[str] = Field(default_factory=list)
