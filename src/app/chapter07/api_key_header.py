from typing import Any

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.security import APIKeyHeader


API_TOKEN = "SECRET_API_TOKEN"  # noqa: S105


app = FastAPI()
api_key_header = APIKeyHeader(name="Token")


@app.get("/protected-route-1")
async def protected_route_1(
    token: str = Depends(api_key_header),
) -> dict[str, Any]:
    if token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return {"hello": "world"}


async def api_token(token: str = Depends(APIKeyHeader(name="Token"))) -> None:
    if token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@app.get("/protected-route-2", dependencies=[Depends(api_token)])
async def protected_route_2() -> dict[str, Any]:
    return {"hello": "world"}
