import pytest

from app.operations import OperationFactory
from app.exceptions import DivisionByZeroError


def test_integer_division():
    operation = OperationFactory.create_operation("int_divide")
    assert operation.execute(10, 3) == 3


def test_integer_division_negative():
    operation = OperationFactory.create_operation("int_divide")
    assert operation.execute(-10, 3) == -3


def test_integer_division_by_zero():
    operation = OperationFactory.create_operation("int_divide")
    with pytest.raises(DivisionByZeroError):
        operation.execute(10, 0)