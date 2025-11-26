from temp import add


def test_add() -> None:
    # Given
    a, b = 1, 1

    # Whene
    result = add(a, b)

    # Then
    assert result == 2
