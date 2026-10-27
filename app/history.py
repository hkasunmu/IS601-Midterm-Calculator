
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd

from app.exceptions import HistoryError


class CalculationHistory:
    """Manages calculator history using a pandas DataFrame."""

    def __init__(self, filename="calculation_history.csv"):
        self.filename = Path(filename)

        self.columns = [
            "operation",
            "operand1",
            "operand2",
            "result",
            "timestamp",
        ]

        self.history = pd.DataFrame(columns=self.columns)

    def add_record(
        self, operation, operand1, operand2, result, timestamp=None
    ):
        """Add a calculation to history with a timestamp."""

        if timestamp is None:
            timestamp = datetime.now(
                timezone.utc
            ).isoformat(timespec="seconds")

        new_record = pd.DataFrame(
            [{
                "operation": operation,
                "operand1": operand1,
                "operand2": operand2,
                "result": result,
                "timestamp": timestamp,
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
            self.filename.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            self.history.to_csv(
                self.filename,
                index=False
            )

        except Exception as exc:
            raise HistoryError(
                f"Unable to save history: {exc}"
            ) from exc

    def load(self):
        """Load calculation history from a CSV file."""
        try:
            if self.filename.exists():
                data = pd.read_csv(self.filename)

                required_columns = [
                    "operation",
                    "operand1",
                    "operand2",
                    "result",
                ]

                for column in required_columns:
                    if column not in data.columns:
                        raise ValueError(
                            f"Missing history column: {column}"
                        )

                # Support older CSV files without timestamps
                if "timestamp" not in data.columns:
                    data["timestamp"] = None

                self.history = data[self.columns].copy()

            return self.history.copy()

        except Exception as exc:
            raise HistoryError(
                f"Unable to load history: {exc}"
            ) from exc
