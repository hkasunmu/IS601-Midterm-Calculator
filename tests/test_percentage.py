import pytest

from app.operations import OperationFactory
from app.exceptions import DivisionByZeroError


def test_percentage():
    operation = OperationFactory.create_operation("percent")
    assert operation.execute(25, 100) == 25.0


def test_percentage_negative():
    operation = OperationFactory.create_operation("percent")
    assert operation.execute(-25, 100) == -25.0


def test_percentage_division_by_zero():
    operation = OperationFactory.create_operation("percent")
    with pytest.raises(DivisionByZeroError):
        operation.execute(25, 0)