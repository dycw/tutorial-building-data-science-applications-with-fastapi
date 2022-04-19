from datetime import datetime
from datetime import timedelta

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from tortoise.fields import CharField
from tortoise.fields import DatetimeField
from tortoise.fields import ForeignKeyField
from tortoise.fields import IntField
from tortoise.models import Model
from tortoise.timezone import now

from app.chapter7.csrf.password import generate_token


class UserBase(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int


class UserDB(User):
    hashed_password: str


class UserTortoise(Model):
    id = IntField(pk=True, generated=True)
    email = CharField(index=True, unique=True, null=False, max_length=255)
    hashed_password = CharField(null=False, max_length=255)

    class Meta:  # type: ignore
        table = "user"


def get_expiration_date(duration_seconds: int = 86400) -> datetime:
    return now() + timedelta(seconds=duration_seconds)


class AccessToken(BaseModel):
    user_id: int
    access_token: str = Field(default_factory=generate_token)
    expiration_date: datetime = Field(default_factory=get_expiration_date)

    def max_age(self) -> int:
        delta = self.expiration_date - now()
        return int(delta.total_seconds())

    class Config:
        orm_mode = True


class AccessTokenTortoise(Model):
    access_token = CharField(pk=True, max_length=255)
    user = ForeignKeyField("models.UserTortoise", null=False)
    expiration_date = DatetimeField(null=False)

    class Meta:  # type: ignore
        table = "access_tokens"
