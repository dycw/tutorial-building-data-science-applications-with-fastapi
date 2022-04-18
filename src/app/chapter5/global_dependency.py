from typing import Any

from fastapi import Depends
from fastapi import FastAPI
from fastapi import Header
from fastapi import HTTPException
from fastapi import status


def secret_header(secret_header: str | None = Header(None)) -> None:
    if not secret_header or secret_header != "SECRET_VALUE":  # noqa: S105
        raise HTTPException(status.HTTP_403_FORBIDDEN)


app = FastAPI(dependencies=[Depends(secret_header)])


@app.get("/route1")
async def route1() -> dict[str, Any]:
    return {"route": "route1"}


@app.get("/route2")
async def route2() -> dict[str, Any]:
    return {"route": "route2"}
