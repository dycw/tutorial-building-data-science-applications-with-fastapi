from tortoise.exceptions import DoesNotExist

from app.chapter7.authentication.models import AccessToken
from app.chapter7.authentication.models import AccessTokenTortoise
from app.chapter7.authentication.models import UserDB
from app.chapter7.authentication.models import UserTortoise
from app.chapter7.authentication.password import verify_password


async def authenticate(email: str, password: str) -> UserDB | None:
    try:
        user = await UserTortoise.get(email=email)
    except DoesNotExist:
        return None
    if verify_password(password, user.hashed_password):
        return UserDB.from_orm(user)
    else:
        return None


async def create_access_token(user: UserDB) -> AccessToken:
    access_token = AccessToken(user_id=user.id)
    access_token_tortoise = await AccessTokenTortoise.create(
        **access_token.dict()
    )
    return AccessToken.from_orm(access_token_tortoise)
