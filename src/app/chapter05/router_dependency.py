from typing import Any
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Header
from fastapi import status


def secret_header(secret_header: Optional[str] = Header(None)) -> None:
    if not secret_header or secret_header != "SECRET_VALUE":  # noqa: S105
        raise HTTPException(status.HTTP_403_FORBIDDEN)


router_1 = APIRouter(dependencies=[Depends(secret_header)])


@router_1.get("/route1")
async def router_route1() -> dict[str, Any]:
    return {"route": "route1"}


@router_1.get("/route2")
async def router_route2() -> dict[str, Any]:
    return {"route": "route2"}


app_1 = FastAPI()
app_1.include_router(router_1, prefix="/router")


router_2 = APIRouter()


@router_2.get("/route3")
async def router_route3() -> dict[str, Any]:
    return {"route": "route3"}


@router_2.get("/route4")
async def router_route4() -> dict[str, Any]:
    return {"route": "route3"}


app_2 = FastAPI()
app_2.include_router(
    router_2, prefix="/router", dependencies=[Depends(secret_header)]
)
