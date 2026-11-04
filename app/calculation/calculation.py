
from app.operation.operations import (
    Addition,
    Subtraction,
    Multiplication,
    Division,
)

from app.operations import OperationFactory


class Calculation:
    """Represents a single calculator calculation."""

    def __init__(self, a, b, operation, timestamp=None):
        self.a = a
        self.b = b
        self.operation = operation
        self.timestamp = timestamp
        self.result = None
        self.operation_name = None

    def perform(self):
        """Perform the requested calculation."""

        if isinstance(self.operation, type):
            if hasattr(self.operation, "calculate"):
                return self.operation.calculate(
                    self.a, self.b
                )

            return self.operation().execute(
                self.a, self.b
            )

        if hasattr(self.operation, "execute"):
            return self.operation.execute(
                self.a, self.b
            )

        return self.operation.calculate(
            self.a, self.b
        )

    def __str__(self):
        """Return a readable calculation."""

        result = self.perform()

        operation_name = (
            self.operation.__name__
            if isinstance(self.operation, type)
            else type(self.operation).__name__
        )

        return (
            f"{self.a} {operation_name} "
            f"{self.b} = {result}"
        )

    @classmethod
    def from_record(cls, record):
        """Restore a Calculation object from a CSV record."""

        operation_name = str(
            record["operation"]
        ).lower().strip()

        calculation = CalculationFactory.create_calculation(
            operation_name,
            float(record["operand1"]),
            float(record["operand2"]),
        )

        calculation.timestamp = record.get("timestamp")
        calculation.result = float(record["result"])
        calculation.operation_name = operation_name

        return calculation


class CalculationFactory:
    """Creates calculation objects for supported operations."""

    operations = {
        "add": Addition,
        "subtract": Subtraction,
        "multiply": Multiplication,
        "divide": Division,
        "power": OperationFactory.operations["power"],
        "root": OperationFactory.operations["root"],
        "modulus": OperationFactory.operations["modulus"],
        "int_divide": OperationFactory.operations["int_divide"],
        "percent": OperationFactory.operations["percent"],
        "abs_diff": OperationFactory.operations["abs_diff"],
    }

    @classmethod
    def create_calculation(cls, operation_name, a, b):
        """Create a Calculation object."""

        operation_name = operation_name.lower().strip()

        if operation_name not in cls.operations:
            raise ValueError(
                f"Unknown operation: {operation_name}"
            )

        operation = cls.operations[operation_name]

        calculation = Calculation(
            a,
            b,
            operation,
        )

        calculation.operation_name = operation_name

        return calculation
