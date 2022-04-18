from app.chapter4.pydantic_types import User
from pydantic import ValidationError
from pytest import raises


def test_invalid_email() -> None:
    with raises(
        ValidationError, match=r"email\n\s*value is not a valid email address"
    ):
        User(email="joe", website="https://www.example.com")  # type: ignore


def test_invalid_url() -> None:
    with raises(
        ValidationError, match=r"website\n\s*invalid or missing URL scheme"
    ):
        User(email="jdoe@example.com", website="jdoe")  # type: ignore


def test_valid() -> None:
    user = User(
        email="jdoe@example.com", website="https://www.example.com"  # type: ignore
    )
    assert isinstance(user, User)
