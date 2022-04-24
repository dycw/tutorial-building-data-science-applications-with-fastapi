from typing import Any
from typing import cast

from fastapi import Depends
from fastapi import FastAPI
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist
from tortoise.exceptions import IntegrityError
from tortoise.timezone import now

from app.chapter07.authentication.authentication import authenticate
from app.chapter07.authentication.authentication import create_access_token
from app.chapter07.authentication.models import AccessTokenTortoise
from app.chapter07.authentication.models import User
from app.chapter07.authentication.models import UserCreate
from app.chapter07.authentication.models import UserDB
from app.chapter07.authentication.models import UserTortoise
from app.chapter07.authentication.password import get_password_hash


async def get_current_user(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/token")),
) -> UserTortoise:
    try:
        access_token = cast(
            AccessTokenTortoise,
            await AccessTokenTortoise.get(
                access_token=token, expiration_date__gte=now()
            ).prefetch_related("user"),
        )
        return cast(UserTortoise, access_token.user)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


app = FastAPI()


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    try:
        user_tortoise = await UserTortoise.create(
            **user.dict(), hashed_password=hashed_password
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )
    return User.from_orm(user_tortoise)


@app.post("/token")
async def create_token(
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
) -> dict[str, Any]:
    email = form_data.username
    password = form_data.password
    if not (user := await authenticate(email, password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = await create_access_token(user)
    return {"access_token": token.access_token, "token_type": "bearer"}


@app.get("/protected-route", response_model=User)
async def protected_route(user: UserDB = Depends(get_current_user)) -> User:
    return User.from_orm(user)


TORTOISE_ORM = {
    "connections": {"default": "sqlite://chapter07_authentication.db"},
    "apps": {
        "models": {
            "models": ["app.chapter07.authentication.models"],
            "default_connection": "default",
        }
    },
    "use_tz": True,
}


register_tortoise(
    app, config=TORTOISE_ORM, generate_schemas=True, add_exception_handlers=True
)
