from typing import Any

from fastapi import FastAPI
from fastapi import Header


app = FastAPI()


@app.get("/")
async def header(user_agent: str = Header(...)) -> dict[str, Any]:
    return {"user_agent": user_agent}
