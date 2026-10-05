import pytest

from app.exceptions import InvalidInputError, InvalidOperationError
from app.input_validators import validate_number, validate_operation


@pytest.mark.parametrize(
    "value,expected",
    [
        ("10", 10.0),
        ("5.5", 5.5),
        ("-3", -3.0),
        (0, 0.0),
        (25, 25.0),
    ],
)
def test_validate_number_valid(value, expected):
    assert validate_number(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "hello",
        "abc123",
        "",
        None,
    ],
)
def test_validate_number_invalid(value):
    with pytest.raises(InvalidInputError):
        validate_number(value)


@pytest.mark.parametrize(
    "operation",
    [
        "add",
        "subtract",
        "multiply",
        "divide",
        "power",
        "root",
    ],
)
def test_validate_operation_valid(operation):
    assert validate_operation(operation) == operation


def test_validate_operation_uppercase():
    assert validate_operation("ADD") == "add"


def test_validate_operation_spaces():
    assert validate_operation("  multiply  ") == "multiply"


@pytest.mark.parametrize(
    "operation",
    [
        "fake",
        "modulus",
        "plus",
    ],
)
def test_validate_operation_invalid(operation):
    with pytest.raises(InvalidOperationError):
        validate_operation(operation)