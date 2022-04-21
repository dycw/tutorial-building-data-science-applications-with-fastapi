from typing import Any

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def hello_world() -> dict[str, Any]:
    return {"hello": "world"}


@app.on_event("startup")  # type: ignore
async def startup() -> None:
    pass


@app.on_event("shutdown")  # type: ignore
async def shutdown() -> None:
    pass
