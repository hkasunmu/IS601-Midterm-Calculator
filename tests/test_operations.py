import pytest

from app.operation.operations import (
    Addition,
    Subtraction,
    Multiplication,
    Division,
)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5),
        (-1, 1, 0),
        (2.5, 1.5, 4.0),
    ],
)
def test_addition(a, b, expected):
    assert Addition.calculate(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 4, 6),
        (5, 10, -5),
        (2.5, 1.5, 1.0),
    ],
)
def test_subtraction(a, b, expected):
    assert Subtraction.calculate(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 6, 30),
        (-2, 3, -6),
        (2.5, 2, 5.0),
    ],
)
def test_multiplication(a, b, expected):
    assert Multiplication.calculate(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (20, 4, 5),
        (10, 2, 5),
        (5, 2, 2.5),
    ],
)
def test_division(a, b, expected):
    assert Division.calculate(a, b) == expected


def test_division_by_zero():
    with pytest.raises(
        ZeroDivisionError,
        match="Cannot divide by zero.",
    ):
        Division.calculate(10, 0)