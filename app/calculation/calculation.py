from app.operation.operations import (
    Addition,
    Subtraction,
    Multiplication,
    Division,
)


class Calculation:
    """Represents one calculator calculation."""

    def __init__(self, a, b, operation):
        self.a = a
        self.b = b
        self.operation = operation

    def perform(self):
        return self.operation.calculate(self.a, self.b)

    def __str__(self):
        result = self.perform()
        return f"{self.a} {self.operation.__name__} {self.b} = {result}"


class CalculationFactory:
    """Creates calculation objects based on user input."""

    operations = {
        "add": Addition,
        "subtract": Subtraction,
        "multiply": Multiplication,
        "divide": Division,
    }

    @classmethod
    def create_calculation(cls, operation_name, a, b):
        operation_name = operation_name.lower()

        if operation_name not in cls.operations:
            raise ValueError(f"Unknown operation: {operation_name}")

        operation = cls.operations[operation_name]

        return Calculation(a, b, operation)