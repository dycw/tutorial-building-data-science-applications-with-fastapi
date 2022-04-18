from datetime import date
from typing import Any

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import root_validator
from pydantic import validator


class Person(BaseModel):
    first_name: str
    last_name: str
    birthdate: date

    @validator("birthdate")
    def valid_birthdate(cls, v: date) -> date:  # noqa: U100
        delta = date.today() - v
        age = delta.days / 365
        if age > 120:
            raise ValueError("You seem a bit too old!")
        return v


class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    password_confirmation: str

    @root_validator()
    def passwords_match(_, values: dict[str, Any]) -> dict[str, Any]:
        password = values.get("password")
        password_confirmation = values.get("password_confirmation")
        if password != password_confirmation:
            raise ValueError("Passwords don't match")
        return values


class Model(BaseModel):
    values: list[int]

    @validator("values", pre=True)
    def split_string_values(cls, v: Any) -> Any:  # noqa: U100
        return v.split(",") if isinstance(v, str) else v
