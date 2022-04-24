from typing import Any

from fastapi import Cookie
from fastapi import FastAPI
from fastapi import Header


app = FastAPI()


@app.get("/1")
async def get_header_1(hello: str = Header(...)) -> dict[str, Any]:
    return {"hello": hello}


@app.get("/2")
async def get_header_2(user_agent: str = Header(...)) -> dict[str, Any]:
    return {"user_agent": user_agent}


@app.get("/3")
async def get_header_3(hello: str | None = Cookie(None)) -> dict[str, Any]:
    return {"hello": hello}
