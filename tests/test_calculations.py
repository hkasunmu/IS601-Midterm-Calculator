import pytest

from app.calculation.calculation import (
    Calculation,
    CalculationFactory,
)
from app.operation.operations import (
    Addition,
    Subtraction,
    Multiplication,
    Division,
)
from app.calculator.calculator import Calculator


@pytest.mark.parametrize(
    "operation, a, b, expected",
    [
        (Addition, 2, 3, 5),
        (Subtraction, 10, 4, 6),
        (Multiplication, 5, 6, 30),
        (Division, 20, 4, 5),
    ],
)
def test_calculation_perform(operation, a, b, expected):
    calculation = Calculation(a, b, operation)
    assert calculation.perform() == expected


@pytest.mark.parametrize(
    "operation_name, a, b, expected",
    [
        ("add", 2, 3, 5),
        ("subtract", 10, 4, 6),
        ("multiply", 5, 6, 30),
        ("divide", 20, 4, 5),
    ],
)
def test_calculation_factory(operation_name, a, b, expected):
    calculation = CalculationFactory.create_calculation(
        operation_name,
        a,
        b,
    )
    assert calculation.perform() == expected


def test_factory_invalid_operation():
    with pytest.raises(
        ValueError,
        match="Unknown operation",
    ):
        CalculationFactory.create_calculation(
            "power",
            2,
            3,
        )


def test_calculator_history():
    calculator = Calculator()

    result = calculator.calculate("add", 5, 3)

    assert result == 8
    assert len(calculator.get_history()) == 1


def test_clear_history():
    calculator = Calculator()

    calculator.calculate("add", 5, 3)
    calculator.clear_history()

    assert calculator.get_history() == []


def test_calculation_string():
    calculation = Calculation(
        5,
        3,
        Addition,
    )

    assert str(calculation) == "5 Addition 3 = 8"