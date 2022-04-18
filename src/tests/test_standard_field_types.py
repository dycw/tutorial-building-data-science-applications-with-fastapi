from app.chapter4.standard_field_types import Gender
from app.chapter4.standard_field_types import Person2
from app.chapter4.standard_field_types import Person3
from pydantic import ValidationError
from pytest import raises


def test_invalid_gender() -> None:
    with raises(
        ValidationError,
        match=r"gender\n\s+value is not a valid enumeration member",
    ):
        Person2(
            first_name="John",
            last_name="Doe",
            gender="INVALID_VALUE",  # type: ignore
            birthdate="1991-01-01",  # type: ignore
            interests=["travel", "sports"],
        )


def test_invalid_birthdate() -> None:
    with raises(ValidationError, match=r"birthdate\n\s+invalid date format"):
        Person2(
            first_name="John",
            last_name="Doe",
            gender=Gender.MALE,
            birthdate="1991-13-42",  # type: ignore
            interests=["travel", "sports"],
        )


def test_person_2() -> None:
    person = Person2(
        first_name="John",
        last_name="Doe",
        gender=Gender.MALE,
        birthdate="1991-01-01",  # type: ignore
        interests=["travel", "sports"],
    )
    assert isinstance(person, Person2)


def test_invalid_country() -> None:
    with raises(ValidationError, match=r"country\n\s+field required"):
        Person3(
            first_name="John",
            last_name="Doe",
            gender=Gender.MALE,
            birthdate="1991-01-01",  # type: ignore
            interests=["travel", "sports"],
            address={  # type: ignore
                "street_address": "12 Squirell Street",
                "postal_code": "424242",
                "city": "Woodtown",
                # Missing country
            },
        )


def test_person_3() -> None:
    person = Person3(
        first_name="John",
        last_name="Doe",
        gender=Gender.MALE,
        birthdate="1991-01-01",  # type: ignore
        interests=["travel", "sports"],
        address={  # type: ignore
            "street_address": "12 Squirell Street",
            "postal_code": "424242",
            "city": "Woodtown",
            "country": "US",
        },
    )
    assert isinstance(person, Person3)
