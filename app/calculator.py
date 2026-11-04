
import math
from numbers import Real
from abc import ABC, abstractmethod

from app.calculator_config import CalculatorConfig
from app.calculator_logger import get_calculator_logger
from app.calculator_memento import MementoManager
from app.history import CalculationHistory
from app.input_validators import validate_number, validate_operation
from app.operations import OperationFactory
from app.exceptions import CalculatorError, HistoryError, InvalidInputError, InvalidOperationError


class CalculatorObserver(ABC):
    """Base class for calculator observers."""

    @abstractmethod
    def update(self, calculator):
        pass  # pragma: no cover


class AutoSaveObserver(CalculatorObserver):
    """Automatically save calculator history when enabled."""

    def update(self, calculator):
        if calculator.config.auto_save:
            calculator.history.save()


class LoggingObserver(CalculatorObserver):
    """Write calculator events to the configured log."""

    def update(self, calculator):
        event = getattr(calculator, "_log_event", None)
        if event:
            calculator.logger.info(event)


class Calculator:
    """Facade providing calculator operations and history management."""

    def __init__(self):
        self.config = CalculatorConfig()
        self.logger = get_calculator_logger(self.config.log_file)
        self._log_event = None

        self.history = CalculationHistory(
            self.config.history_file,
            encoding=self.config.default_encoding,
        )
        try:
            self.history.load()
        except HistoryError as error:
            # A damaged or unreadable history must not prevent startup.
            self.logger.warning("Could not load history; starting empty: %s", error)
            self.history.clear()

        self.memento_manager = MementoManager()
        self.observers = [AutoSaveObserver(), LoggingObserver()]

    def add_observer(self, observer):
        """Register an additional observer."""
        self.observers.append(observer)

    def _notify_observers(self):
        """Notify observers after a successful state change."""
        for observer in self.observers:
            observer.update(self)

    def _get_state(self):
        """Take a snapshot for Undo/Redo."""
        return self.history.get_history().to_dict(orient="records")

    def _restore_state(self, state):
        """Restore snapshot, retaining original calculation timestamps."""
        self.history.clear()
        for record in state:
            self.history.add_record(
                record["operation"],
                record["operand1"],
                record["operand2"],
                record["result"],
                record.get("timestamp"),
            )

    def calculate(self, operation, operand1, operand2):
        """Validate input and calculate, reporting arithmetic errors safely."""
        operation = validate_operation(operation)
        operand1 = validate_number(operand1)
        operand2 = validate_number(operand2)

        if not math.isfinite(operand1) or not math.isfinite(operand2):
            raise InvalidInputError("Inputs must be finite numbers.")
        if (
            abs(operand1) > self.config.max_input_value
            or abs(operand2) > self.config.max_input_value
        ):
            raise InvalidInputError("Input exceeds the maximum allowed value.")

        try:
            strategy = OperationFactory.create_operation(operation)
            result = strategy.execute(operand1, operand2)
            if not isinstance(result, Real) or not math.isfinite(result):
                raise InvalidOperationError(
                    "Calculation produced a non-real or non-finite result."
                )
            result = round(result, self.config.precision)
        except CalculatorError as error:
            self.logger.error("Calculation failed (%s): %s", operation, error)
            raise
        except (ArithmeticError, ValueError, TypeError) as error:
            self.logger.error("Arithmetic error (%s): %s", operation, error)
            raise InvalidOperationError(
                f"Unable to calculate {operation}: {error}"
            ) from error

        # Only successful calculations should change Undo/Redo history.
        self.memento_manager.save_state(self._get_state())
        self.history.add_record(operation, operand1, operand2, result)

        self.history.trim(self.config.max_history)

        self._log_event = (
            f"Calculation: {operation} {operand1}, {operand2} = {result}"
        )
        self._notify_observers()
        return result

    def get_history(self):
        """Return calculation history."""
        return self.history.get_history()

    def clear(self):
        """Clear calculation history, retaining Undo state."""
        self.memento_manager.save_state(self._get_state())
        self.history.clear()
        self._log_event = "History cleared"
        self._notify_observers()

    def undo(self):
        """Undo the most recent history change."""
        current_state = self._get_state()
        previous_state = self.memento_manager.undo(current_state)
        self._restore_state(previous_state)
        self._log_event = "Undo completed"
        self._notify_observers()
        return self.get_history()

    def redo(self):
        """Redo the last undone history change."""
        current_state = self._get_state()
        next_state = self.memento_manager.redo(current_state)
        self._restore_state(next_state)
        self._log_event = "Redo completed"
        self._notify_observers()
        return self.get_history()

    def save(self):
        """Save calculation history to CSV."""
        self.history.save()

    def load(self):
        """Load calculation history from CSV."""
        return self.history.load()
