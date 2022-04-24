from typing import Any

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Header
from fastapi import status


def secret_header(secret_header: str | None = Header(None)) -> None:
    if not secret_header or secret_header != "SECRET_VALUE":  # noqa: S105
        raise HTTPException(status.HTTP_403_FORBIDDEN)


app = FastAPI()


@app.get("/protected-route", dependencies=[Depends(secret_header)])
async def protected_route() -> dict[str, Any]:
    return {"hello": "world"}
