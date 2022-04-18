from typing import Any

from fastapi import Body
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


@app.post("/users-1")
async def create_user_1(name: str = Body(...), age: int = Body(...)) -> dict[str, Any]:
    return {"name": name, "age": age}


class User(BaseModel):
    name: str
    age: int


@app.post("/users-2")
async def create_user_2(user: User) -> User:
    return user


class Company(BaseModel):
    name: str


@app.post("/users-3")
async def create_user_3(user: User, company: Company) -> dict[str, Any]:
    return {"user": user, "company": company}


@app.post("/users-4")
async def create_user_4(
    user: User, priority: int = Body(..., ge=1, le=3)
) -> dict[str, Any]:
    return {"user": user, "priority": priority}
