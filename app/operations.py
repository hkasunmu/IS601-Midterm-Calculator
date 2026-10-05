from abc import ABC, abstractmethod
from app.exceptions import DivisionByZeroError, InvalidOperationError


class Operation(ABC):
    """Base class for calculator operations."""

    @abstractmethod
    def execute(self, a, b):
        pass  # pragma: no cover


class AddOperation(Operation):
    def execute(self, a, b):
        return a + b


class SubtractOperation(Operation):
    def execute(self, a, b):
        return a - b


class MultiplyOperation(Operation):
    def execute(self, a, b):
        return a * b


class DivideOperation(Operation):
    def execute(self, a, b):
        if b == 0:
            raise DivisionByZeroError("Cannot divide by zero.")
        return a / b


class PowerOperation(Operation):
    def execute(self, a, b):
        return a ** b


class RootOperation(Operation):
    def execute(self, a, b):
        if b == 0:
            raise InvalidOperationError("Root value cannot be zero.")

        if a < 0 and b % 2 == 0:
            raise InvalidOperationError(
                "Cannot calculate an even root of a negative number."
            )

        if a < 0:
            return -((-a) ** (1 / b))

        return a ** (1 / b)


class OperationFactory:
    """Factory that creates operation objects."""

    operations = {
        "add": AddOperation,
        "subtract": SubtractOperation,
        "multiply": MultiplyOperation,
        "divide": DivideOperation,
        "power": PowerOperation,
        "root": RootOperation,
    }

    @classmethod
    def create_operation(cls, operation_name):
        if operation_name not in cls.operations:
            raise InvalidOperationError(
                f"Invalid operation: {operation_name}"
            )

        return cls.operations[operation_name]()