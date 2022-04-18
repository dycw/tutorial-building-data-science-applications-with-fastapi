from app.chapter4.standard_field_types import Gender
from app.chapter4.standard_field_types import Person3


def test_dict() -> None:
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
    person_dict = person.dict()
    assert person_dict["first_name"] == "John"
    assert person_dict["address"]["street_address"] == "12 Squirell Street"


def test_include() -> None:
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
    person_include = person.dict(include={"first_name", "last_name"})
    assert set(person_include) == {"first_name", "last_name"}


def test_exclude() -> None:
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
    person_exclude = person.dict(exclude={"birthdate", "interests"})
    assert set(person_exclude) == {
        "first_name",
        "last_name",
        "gender",
        "address",
    }


def test_nested_include() -> None:
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
    person_exclude = person.dict(
        include={
            "first_name": ...,
            "last_name": ...,
            "address": {"city", "country"},
        }
    )
    assert set(person_exclude) == {"first_name", "last_name", "address"}
    assert set(person_exclude["address"]) == {"city", "country"}
