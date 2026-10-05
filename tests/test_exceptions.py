from app.exceptions import (
    CalculatorError,
    InvalidInputError,
    DivisionByZeroError,
    InvalidOperationError,
    ConfigurationError,
    HistoryError,
)


def test_invalid_input_error_inherits_calculator_error():
    assert issubclass(InvalidInputError, CalculatorError)


def test_division_by_zero_error_inherits_calculator_error():
    assert issubclass(DivisionByZeroError, CalculatorError)


def test_invalid_operation_error_inherits_calculator_error():
    assert issubclass(InvalidOperationError, CalculatorError)


def test_configuration_error_inherits_calculator_error():
    assert issubclass(ConfigurationError, CalculatorError)


def test_history_error_inherits_calculator_error():
    assert issubclass(HistoryError, CalculatorError)


def test_exception_message():
    error = InvalidInputError("Invalid number")
    assert str(error) == "Invalid number"