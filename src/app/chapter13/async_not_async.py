from time import sleep
from typing import Any

from fastapi import FastAPI


app = FastAPI()


@app.get("/fast")
async def fast() -> dict[str, Any]:
    return {"endpoint": "fast"}


@app.get("/slow-async")
async def slow_async() -> dict[str, Any]:
    sleep(10)
    return {"endpoint": "slow-async"}


@app.get("/slow-sync")
def slow_sync() -> dict[str, Any]:
    sleep(10)
    return {"endpoint": "slow-sync"}
