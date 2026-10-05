from app.calculation.calculation import CalculationFactory


class Calculator:
    """Manages calculations and calculation history."""

    def __init__(self):
        self.history = []

    def calculate(self, operation_name, a, b):
        """Create and perform a calculation."""
        calculation = CalculationFactory.create_calculation(
            operation_name, a, b
        )

        result = calculation.perform()

        self.history.append(calculation)

        return result

    def get_history(self):
        """Return the calculations performed during this session."""
        return self.history.copy()

    def clear_history(self):
        """Remove all calculations from history."""
        self.history.clear()