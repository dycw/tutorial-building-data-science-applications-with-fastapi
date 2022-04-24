from typing import Any

from fastapi import FastAPI
from fastapi import Request


app = FastAPI()


@app.get("/")
async def get() -> dict[str, Any]:
    return {"detail": "GET response"}


@app.post("/")
async def post(request: Request) -> dict[str, Any]:
    json = await request.json()
    return {"detail": "POST response", "input_payload": json}
