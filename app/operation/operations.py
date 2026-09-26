class Addition:
    """Performs addition."""

    @staticmethod
    def calculate(a, b):
        return a + b


class Subtraction:
    """Performs subtraction."""

    @staticmethod
    def calculate(a, b):
        return a - b


class Multiplication:
    """Performs multiplication."""

    @staticmethod
    def calculate(a, b):
        return a * b


class Division:
    """Performs division."""

    @staticmethod
    def calculate(a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b