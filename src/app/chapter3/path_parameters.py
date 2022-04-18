from enum import auto
from enum import Enum
from typing import Any

from fastapi import FastAPI
from fastapi import Path


app = FastAPI()


@app.get("/users1/{id}")
async def get_user_1(id: int) -> dict[str, Any]:
    return {"id": id}


@app.get("/users2/{id}")
async def get_user_2(type: str, id: int) -> dict[str, Any]:
    return {"type": type, "id": id}


class UserType(str, Enum):
    def _generate_next_value_(name, *_: Any) -> str:  # type: ignore
        return name

    standard = auto()
    admin = auto()


@app.get("/users3/{type}/{id}")
async def get_user_3(type: UserType, id: int) -> dict[str, Any]:
    return {"type": type, "id": id}


@app.get("/users4/{id}")
async def get_user_4(id: int = Path(..., ge=1)) -> dict[str, Any]:
    return {"id": id}


@app.get("/license-plates-1/{license}")
async def get_license_plate_1(
    license: str = Path(..., min_length=9, max_length=9)
) -> dict[str, Any]:
    return {"license": license}


@app.get("/license-plates-2/{license}")
async def get_license_plate_2(
    license: str = Path(..., regex=r"^\w{2}-\d{3}-\w{2}$")
) -> dict[str, Any]:
    return {"license": license}
