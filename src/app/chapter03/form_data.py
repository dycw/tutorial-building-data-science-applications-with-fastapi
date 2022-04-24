from typing import Any

from fastapi import FastAPI
from fastapi import Form


app = FastAPI()


@app.post("/users")
async def create_user(
    name: str = Form(...), age: int = Form(...)
) -> dict[str, Any]:
    return {"name": name, "age": age}
