from typing import Any
from typing import cast

from fastapi import Depends
from fastapi import FastAPI
from fastapi import Form
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security.api_key import APIKeyCookie
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response
from starlette_csrf.middleware import CSRFMiddleware
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist
from tortoise.exceptions import IntegrityError
from tortoise.timezone import now

from app.chapter07.csrf.authentication import authenticate
from app.chapter07.csrf.authentication import create_access_token
from app.chapter07.csrf.models import AccessTokenTortoise
from app.chapter07.csrf.models import User
from app.chapter07.csrf.models import UserCreate
from app.chapter07.csrf.models import UserTortoise
from app.chapter07.csrf.models import UserUpdate
from app.chapter07.csrf.password import get_password_hash


TOKEN_COOKIE_NAME = "token"  # noqa: S105
CSRF_TOKEN_SECRET = "my-token-secret"  # noqa: S105


async def get_current_user(
    token: str = Depends(APIKeyCookie(name=TOKEN_COOKIE_NAME)),
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    CSRFMiddleware,
    secret=CSRF_TOKEN_SECRET,
    sensitive_cookies={TOKEN_COOKIE_NAME},
    cookie_domain="localhost",
)


@app.get("/csrf")
async def csrf() -> None:
    return None


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


@app.post("/login")
async def login(
    response: Response, email: str = Form(...), password: str = Form(...)
) -> dict[str, Any]:
    if not (user := await authenticate(email, password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = await create_access_token(user)
    response.set_cookie(
        TOKEN_COOKIE_NAME,
        token.access_token,
        max_age=token.max_age(),
        secure=True,
        httponly=True,
        samesite="lax",
    )
    return {"access_token": token.access_token, "token_type": "bearer"}


@app.get("/me", response_model=User)
async def get_me(user: UserTortoise = Depends(get_current_user)) -> User:
    return User.from_orm(user)


@app.post("/me", response_model=User)
async def update_me(
    user_update: UserUpdate, user: UserTortoise = Depends(get_current_user)
) -> User:
    _ = user.update_from_dict(user_update.dict(exclude_unset=True))
    await user.save()
    return User.from_orm(user)


TORTOISE_ORM = {
    "connections": {"default": "sqlite://chapter07_csrf.db"},
    "apps": {
        "models": {
            "models": ["app.chapter07.csrf.models"],
            "default_connection": "default",
        }
    },
    "use_tz": True,
}


register_tortoise(
    app, config=TORTOISE_ORM, generate_schemas=True, add_exception_handlers=True
)
