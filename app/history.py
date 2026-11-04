
import os
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd
from dotenv import load_dotenv

from app.calculation.calculation import Calculation
from app.exceptions import HistoryError


class CalculationHistory:
    """Manage calculation history and CSV persistence."""

    def __init__(
        self,
        filename="calculation_history.csv",
        encoding=None
    ):
        load_dotenv()

        self.filename = Path(filename)

        self.encoding = (
            encoding
            if encoding is not None
            else os.getenv(
                "CALCULATOR_DEFAULT_ENCODING",
                "utf-8"
            )
        )

        self.columns = [
            "operation",
            "operand1",
            "operand2",
            "result",
            "timestamp",
        ]

        self.history = pd.DataFrame(
            columns=self.columns
        )

        self.calculations = []

    def add_record(
        self,
        operation,
        operand1,
        operand2,
        result,
        timestamp=None
    ):
        """Add a calculation to history."""

        if timestamp is None:
            timestamp = datetime.now(
                timezone.utc
            ).isoformat(timespec="seconds")

        record = {
            "operation": operation,
            "operand1": operand1,
            "operand2": operand2,
            "result": result,
            "timestamp": timestamp,
        }

        new_record = pd.DataFrame([record])

        self.history = pd.concat(
            [self.history, new_record],
            ignore_index=True
        )

    def get_history(self):
        """Return calculation history as a DataFrame."""
        return self.history.copy()

    def get_calculations(self):
        """Return actual Calculation objects."""
        return [
            Calculation.from_record(record)
            for record in self.history.to_dict(
                orient="records"
            )
        ]

    def clear(self):
        """Clear calculation history."""
        self.history = pd.DataFrame(
            columns=self.columns
        )
        self.calculations = []

    def save(self):
        """Save history to a CSV file."""
        try:
            self.filename.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            self.history.to_csv(
                self.filename,
                index=False,
                encoding=self.encoding
            )

        except Exception as exc:
            raise HistoryError(
                f"Unable to save history: {exc}"
            ) from exc

    def load(self):
        """Load CSV history and restore Calculation objects."""
        try:
            if not self.filename.exists():
                return self.history.copy()

            data = pd.read_csv(
                self.filename,
                encoding=self.encoding
            )

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

            # Support older CSV files
            if "timestamp" not in data.columns:
                data["timestamp"] = None

            data = data[self.columns].copy()

            # Reconstruct actual Calculation objects
            restored_calculations = [
                Calculation.from_record(record)
                for record in data.to_dict(
                    orient="records"
                )
            ]

            self.history = data
            self.calculations = restored_calculations

            return self.history.copy()

        except Exception as exc:
            raise HistoryError(
                f"Unable to load history: {exc}"
            ) from exc
