from enum import Enum
from enum import auto
from typing import Any

from fastapi import FastAPI
from fastapi import Query


app = FastAPI()


@app.get("/users-1")
async def get_user_1(page: int = 1, size: int = 10) -> dict[str, Any]:
    return {"page": page, "size": size}


class UsersFormat(str, Enum):
    def _generate_next_value_(name, *_: Any) -> str:  # type: ignore
        return name

    short = auto()
    full = auto()


@app.get("/users-2")
async def get_user_2(format: UsersFormat) -> dict[str, Any]:
    return {"format": format}


@app.get("/users-3")
async def get_user_3(
    page: int = Query(1, gt=0), size: int = Query(10, le=100)
) -> dict[str, Any]:
    return {"page": page, "size": size}
