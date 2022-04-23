from typing import Any

from fastapi import Depends
from fastapi import FastAPI
from httpx import AsyncClient


app = FastAPI()


class ExternalAPI:
    def __init__(self) -> None:
        super().__init__()
        self.client = AsyncClient(
            base_url="https://dummy.restapiexample.com/api/v1"
        )

    async def __call__(self) -> Any:
        async with self.client as client:
            return (await client.get("employees")).json()


external_api = ExternalAPI()


@app.get("/employees")
async def external_employees(
    employees: dict[str, Any] = Depends(external_api)
) -> dict[str, Any]:
    return employees
