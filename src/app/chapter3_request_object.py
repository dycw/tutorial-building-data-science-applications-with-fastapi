from typing import Any

from fastapi import FastAPI
from fastapi import Request


app = FastAPI()


@app.get("/")
async def get_request_object(request: Request) -> dict[str, Any]:
    return {"path": request.url.path}
