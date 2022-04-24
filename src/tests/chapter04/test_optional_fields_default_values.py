from time import sleep

from pytest import raises

from app.chapter04.optional_fields_default_values import Model
from app.chapter04.optional_fields_default_values import UserProfile


def test_user_profile() -> None:
    user = UserProfile(nickname="joe")
    assert isinstance(user, UserProfile)
    assert user.location is None
    assert user.subscribed_newsletter is True


def test_model() -> None:
    o1 = Model()
    sleep(0.1)
    o2 = Model()
    with raises(AssertionError):
        assert o1.d < o2.d
