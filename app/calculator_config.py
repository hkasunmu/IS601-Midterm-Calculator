import os
from dotenv import load_dotenv

from app.exceptions import ConfigurationError


class CalculatorConfig:
    """Manages calculator configuration settings."""

    def __init__(self):
        load_dotenv()

        self.history_file = os.getenv(
            "CALCULATOR_HISTORY_FILE",
            "calculation_history.csv"
        )

        self.auto_save = os.getenv(
            "CALCULATOR_AUTO_SAVE",
            "true"
        ).lower() == "true"

        self.max_history = self._get_max_history()

    def _get_max_history(self):
        """Validate and return the maximum history size."""
        try:
            value = int(
                os.getenv("CALCULATOR_MAX_HISTORY", "100")
            )

            if value <= 0:
                raise ValueError

            return value

        except ValueError as exc:
            raise ConfigurationError(
                "CALCULATOR_MAX_HISTORY must be a positive integer."
            ) from exc