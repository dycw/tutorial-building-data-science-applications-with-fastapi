from app.chapter04.custom_validation import Model


def test_model() -> None:
    m = Model(values="1,2,3")  # type: ignore
    assert m.values == [1, 2, 3]
