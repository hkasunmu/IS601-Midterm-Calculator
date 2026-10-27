
from abc import ABC, abstractmethod

from app.calculator_config import CalculatorConfig
from app.calculator_logger import get_calculator_logger
from app.calculator_memento import MementoManager
from app.history import CalculationHistory
from app.input_validators import validate_number, validate_operation
from app.operations import OperationFactory


class CalculatorObserver(ABC):
    """Base class for calculator observers."""

    @abstractmethod
    def update(self, calculator):
        pass  # pragma: no cover


class AutoSaveObserver(CalculatorObserver):
    """Automatically saves calculator history."""

    def update(self, calculator):
        if calculator.config.auto_save:
            calculator.history.save()


class LoggingObserver(CalculatorObserver):
    """Logs calculator events to a file."""

    def update(self, calculator):
        message = getattr(calculator, "_log_event", None)

        if message:
            calculator.logger.info(message)


class Calculator:
    """Facade that provides a simple interface to the calculator."""

    def __init__(self):
        self.config = CalculatorConfig()

        # Set up calculator logging
        self.logger = get_calculator_logger(
            self.config.log_file
        )

        self._log_event = None

        # Set up calculation history
        self.history = CalculationHistory(
            self.config.history_file
        )

        self.history.load()

        # Set up undo and redo
        self.memento_manager = MementoManager()

        # Register calculator observers
        self.observers = [
            AutoSaveObserver(),
            LoggingObserver(),
        ]

    def add_observer(self, observer):
        """Add an observer."""
        self.observers.append(observer)

    def _notify_observers(self):
        """Notify all observers."""
        for observer in self.observers:
            observer.update(self)

    def _get_state(self):
        """Return calculator history as a state snapshot."""
        return self.history.get_history().to_dict(
            orient="records"
        )

    def _restore_state(self, state):
        """Restore calculator history from a saved state."""
        self.history.clear()

        for record in state:
            self.history.add_record(
                record["operation"],
                record["operand1"],
                record["operand2"],
                record["result"],
            )

    def calculate(self, operation, operand1, operand2):
        """Perform a calculation."""

        # Validate operation and numbers
        operation = validate_operation(operation)

        operand1 = validate_number(operand1)
        operand2 = validate_number(operand2)

        # Save current state for undo
        self.memento_manager.save_state(
            self._get_state()
        )

        # Create the requested operation
        strategy = OperationFactory.create_operation(
            operation
        )

        # Perform calculation
        result = strategy.execute(
            operand1,
            operand2
        )

        # Save calculation to history
        self.history.add_record(
            operation,
            operand1,
            operand2,
            result,
        )

        # Limit history size
        if len(self.history.history) > self.config.max_history:
            self.history.history = (
                self.history.history
                .tail(self.config.max_history)
                .reset_index(drop=True)
            )

        # Log the calculation
        self._log_event = (
            f"Calculation: {operation} "
            f"{operand1}, {operand2} = {result}"
        )

        # Notify logging and auto-save observers
        self._notify_observers()

        return result

    def get_history(self):
        """Return calculation history."""
        return self.history.get_history()

    def clear(self):
        """Clear calculator history."""

        self.memento_manager.save_state(
            self._get_state()
        )

        self.history.clear()

        # Log history clearing
        self._log_event = "History cleared"

        self._notify_observers()

    def undo(self):
        """Undo the most recent change."""

        current_state = self._get_state()

        previous_state = self.memento_manager.undo(
            current_state
        )

        self._restore_state(previous_state)

        # Log undo
        self._log_event = "Undo completed"

        self._notify_observers()

        return self.get_history()

    def redo(self):
        """Redo the most recently undone change."""

        current_state = self._get_state()

        next_state = self.memento_manager.redo(
            current_state
        )

        self._restore_state(next_state)

        # Log redo
        self._log_event = "Redo completed"

        self._notify_observers()

        return self.get_history()

    def save(self):
        """Manually save history."""
        self.history.save()

    def load(self):
        """Manually load history."""
        return self.history.load()
