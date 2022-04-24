from datetime import date
from enum import Enum
from enum import auto
from typing import Any

from pydantic import BaseModel


class Person1(BaseModel):
    first_name: str
    last_name: str
    age: int


class Gender(str, Enum):
    def _generate_next_value_(name, *_: Any) -> str:  # type: ignore
        return name

    MALE = auto()
    FEMALE = auto()
    NON_BINARY = auto()


class Person2(BaseModel):
    first_name: str
    last_name: str
    gender: Gender
    birthdate: date
    interests: list[str]


class Address(BaseModel):
    street_address: str
    postal_code: str
    city: str
    country: str


class Person3(BaseModel):
    first_name: str
    last_name: str
    gender: Gender
    birthdate: date
    interests: list[str]
    address: Address
