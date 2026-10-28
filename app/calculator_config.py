
import os
import math
import codecs

from dotenv import load_dotenv
from app.exceptions import ConfigurationError


class CalculatorConfig:
    """Manages calculator configuration settings."""

    def __init__(self):
        load_dotenv()

        # Logging settings
        self.log_dir = os.getenv(
            "CALCULATOR_LOG_DIR", "logs"
        )

        self.log_file = os.getenv(
            "CALCULATOR_LOG_FILE",
            os.path.join(self.log_dir, "calculator.log")
        )

        # History settings
        self.history_dir = os.getenv(
            "CALCULATOR_HISTORY_DIR", "."
        )

        default_history_file = (
            "calculation_history.csv"
            if self.history_dir == "."
            else os.path.join(
                self.history_dir, "calculation_history.csv"
            )
        )

        self.history_file = os.getenv(
            "CALCULATOR_HISTORY_FILE",
            default_history_file
        )

        self.auto_save = os.getenv(
            "CALCULATOR_AUTO_SAVE", "true"
        ).lower() == "true"

        self.max_history = self._get_max_history()

        # Calculation settings
        self.precision = self._get_precision()
        self.max_input_value = self._get_max_input_value()

        # File encoding
        self.default_encoding = os.getenv(
            "CALCULATOR_DEFAULT_ENCODING", "utf-8"
        )

        try:
            codecs.lookup(self.default_encoding)
        except LookupError as exc:
            raise ConfigurationError(
                "Invalid file encoding."
            ) from exc

    def _get_max_history(self):
        """Validate maximum history size."""
        try:
            value = int(
                os.getenv(
                    "CALCULATOR_MAX_HISTORY_SIZE",
                    os.getenv("CALCULATOR_MAX_HISTORY", "100")
                )
            )

            if value <= 0:
                raise ValueError

            return value

        except ValueError as exc:
            raise ConfigurationError(
                "CALCULATOR_MAX_HISTORY_SIZE must be a positive integer."
            ) from exc

    def _get_precision(self):
        """Validate decimal precision."""
        try:
            value = int(
                os.getenv("CALCULATOR_PRECISION", "2")
            )

            if not 0 <= value <= 15:
                raise ValueError

            return value

        except ValueError as exc:
            raise ConfigurationError(
                "CALCULATOR_PRECISION must be between 0 and 15."
            ) from exc

    def _get_max_input_value(self):
        """Validate maximum allowed input magnitude."""
        try:
            value = float(
                os.getenv(
                    "CALCULATOR_MAX_INPUT_VALUE",
                    "1000000000"
                )
            )

            if not math.isfinite(value) or value <= 0:
                raise ValueError

            return value

        except ValueError as exc:
            raise ConfigurationError(
                "CALCULATOR_MAX_INPUT_VALUE must be a positive finite number."
            ) from exc
