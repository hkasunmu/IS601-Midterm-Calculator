from pathlib import Path
import pandas as pd

from app.exceptions import HistoryError


class CalculationHistory:
    """Manages calculator history using a pandas DataFrame."""

    def __init__(self, filename="calculation_history.csv"):
        self.filename = Path(filename)
        self.columns = ["operation", "operand1", "operand2", "result"]
        self.history = pd.DataFrame(columns=self.columns)

    def add_record(self, operation, operand1, operand2, result):
        """Add a calculation to history."""
        new_record = pd.DataFrame(
            [{
                "operation": operation,
                "operand1": operand1,
                "operand2": operand2,
                "result": result,
            }]
        )

        self.history = pd.concat(
            [self.history, new_record],
            ignore_index=True
        )

    def get_history(self):
        """Return the current calculation history."""
        return self.history.copy()

    def clear(self):
        """Clear all calculation history."""
        self.history = pd.DataFrame(columns=self.columns)

    def save(self):
        """Save calculation history to a CSV file."""
        try:
            self.history.to_csv(self.filename, index=False)
        except Exception as exc:
            raise HistoryError(
                f"Unable to save history: {exc}"
            ) from exc

    def load(self):
        """Load calculation history from a CSV file."""
        try:
            if self.filename.exists():
                self.history = pd.read_csv(self.filename)
            return self.history.copy()
        except Exception as exc:
            raise HistoryError(
                f"Unable to load history: {exc}"
            ) from exc