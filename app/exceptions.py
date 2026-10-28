
class CalculatorError(Exception):
    """Base exception for calculator errors."""
    pass


class InvalidInputError(CalculatorError):
    """Raised when the user enters invalid input."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when division by zero is attempted."""
    pass


class InvalidOperationError(CalculatorError):
    """Raised when an unsupported operation is entered."""
    pass


class ConfigurationError(CalculatorError):
    """Raised when there is a configuration problem."""
    pass


class HistoryError(CalculatorError):
    """Raised when there is a problem with calculation history."""
    pass
