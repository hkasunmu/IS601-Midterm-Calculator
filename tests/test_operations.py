import pytest

from app.exceptions import DivisionByZeroError, InvalidOperationError
from app.operations import (
    AddOperation,
    SubtractOperation,
    MultiplyOperation,
    DivideOperation,
    PowerOperation,
    RootOperation,
    OperationFactory,
)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (10, 5, 15),
        (-2, 3, 1),
        (0, 0, 0),
    ],
)
def test_add_operation(a, b, expected):
    operation = AddOperation()
    assert operation.execute(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (10, 5, 5),
        (5, 10, -5),
        (0, 0, 0),
    ],
)
def test_subtract_operation(a, b, expected):
    operation = SubtractOperation()
    assert operation.execute(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (10, 5, 50),
        (-2, 3, -6),
        (0, 10, 0),
    ],
)
def test_multiply_operation(a, b, expected):
    operation = MultiplyOperation()
    assert operation.execute(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (10, 5, 2),
        (9, 3, 3),
        (-10, 2, -5),
    ],
)
def test_divide_operation(a, b, expected):
    operation = DivideOperation()
    assert operation.execute(a, b) == expected


def test_divide_by_zero():
    operation = DivideOperation()

    with pytest.raises(DivisionByZeroError):
        operation.execute(10, 0)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 8),
        (5, 2, 25),
        (10, 0, 1),
    ],
)
def test_power_operation(a, b, expected):
    operation = PowerOperation()
    assert operation.execute(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (16, 2, 4),
        (27, 3, 3),
        (81, 4, 3),
    ],
)
def test_root_operation(a, b, expected):
    operation = RootOperation()
    assert operation.execute(a, b) == pytest.approx(expected)


def test_negative_odd_root():
    operation = RootOperation()
    assert operation.execute(-8, 3) == pytest.approx(-2)


def test_zero_root():
    operation = RootOperation()

    with pytest.raises(InvalidOperationError):
        operation.execute(10, 0)


def test_even_root_negative_number():
    operation = RootOperation()

    with pytest.raises(InvalidOperationError):
        operation.execute(-16, 2)


@pytest.mark.parametrize(
    "name,operation_class",
    [
        ("add", AddOperation),
        ("subtract", SubtractOperation),
        ("multiply", MultiplyOperation),
        ("divide", DivideOperation),
        ("power", PowerOperation),
        ("root", RootOperation),
    ],
)
def test_operation_factory(name, operation_class):
    operation = OperationFactory.create_operation(name)
    assert isinstance(operation, operation_class)


def test_operation_factory_invalid_operation():
    with pytest.raises(InvalidOperationError):
        OperationFactory.create_operation("fake")