from typing import Any

from fastapi import Depends
from fastapi import FastAPI
from fastapi import Query


class Pagination1:
    def __init__(self, maximum_limit: int = 100) -> None:
        super().__init__()
        self.maximum_limit = maximum_limit

    async def __call__(
        self, skip: int = Query(0, ge=0), limit: int = Query(10, ge=0)
    ) -> tuple[int, int]:
        capped_limit = min(self.maximum_limit, limit)
        return skip, capped_limit


app = FastAPI()


pagination_1 = Pagination1(maximum_limit=50)


@app.get("/items-1")
async def list_items_1(
    p: tuple[int, int] = Depends(pagination_1)
) -> dict[str, Any]:
    skip, limit = p
    return {"skip": skip, "limit": limit}


class Pagination2:
    def __init__(self, maximum_limit: int = 100) -> None:
        super().__init__()
        self.maximum_limit = maximum_limit

    async def skip_limit(
        self, skip: int = Query(0, ge=0), limit: int = Query(10, ge=0)
    ) -> tuple[int, int]:
        capped_limit = min(self.maximum_limit, limit)
        return skip, capped_limit

    async def page_size(
        self, page: int = Query(1, ge=1), size: int = Query(10, ge=0)
    ) -> tuple[int, int]:
        capped_size = min(self.maximum_limit, size)
        return page, capped_size


pagination_2 = Pagination2(maximum_limit=50)


@app.get("/items-2")
async def list_items_2(
    p: tuple[int, int] = Depends(pagination_2.skip_limit)
) -> dict[str, Any]:
    skip, limit = p
    return {"skip": skip, "limit": limit}


@app.get("/things")
async def list_things(
    p: tuple[int, int] = Depends(pagination_2.page_size)
) -> dict[str, Any]:
    page, size = p
    return {"skip": page, "limit": size}
