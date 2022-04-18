from typing import Any

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def hello() -> dict[str, Any]:
    return {"hello": "world"}
