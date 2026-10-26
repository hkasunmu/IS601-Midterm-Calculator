import pytest

from app.operations import OperationFactory
from app.exceptions import DivisionByZeroError


def test_modulus():
    operation = OperationFactory.create_operation("modulus")
    assert operation.execute(10, 3) == 1


def test_modulus_division_by_zero():
    operation = OperationFactory.create_operation("modulus")
    with pytest.raises(DivisionByZeroError):
        operation.execute(10, 0)