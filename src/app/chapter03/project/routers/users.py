from chapter03.project.db import db
from chapter03.project.models.user import User
from chapter03.project.models.user import UserCreate
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status


router = APIRouter()


@router.get("/")
async def all() -> list[User]:
    return list(db.users.values())


@router.get("/{id}")
async def get(id: int) -> User:
    try:
        return db.users[id]
    except KeyError:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(user_create: UserCreate) -> User:
    new_id = max(db.users.keys() or (0,)) + 1
    user = User(id=new_id, **user_create.dict())
    db.users[new_id] = user
    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int) -> None:
    try:
        _ = db.users.pop(id)
    except KeyError:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
