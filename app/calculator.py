from abc import ABC, abstractmethod

from app.calculator_config import CalculatorConfig
from app.calculator_memento import MementoManager
from app.history import CalculationHistory
from app.input_validators import validate_number, validate_operation
from app.operations import OperationFactory


class CalculatorObserver(ABC):
    @abstractmethod
    def update(self, calculator):
        pass  # pragma: no cover

class AutoSaveObserver(CalculatorObserver):
    """Automatically saves calculator history."""

    def update(self, calculator):
        if calculator.config.auto_save:
            calculator.history.save()


class Calculator:
    """Facade that provides a simple interface to the calculator."""

    def __init__(self):
        self.config = CalculatorConfig()

        self.history = CalculationHistory(
            self.config.history_file
        )

        self.history.load()

        self.memento_manager = MementoManager()

        self.observers = [
            AutoSaveObserver()
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
        operation = validate_operation(operation)

        operand1 = validate_number(operand1)
        operand2 = validate_number(operand2)

        self.memento_manager.save_state(
            self._get_state()
        )

        strategy = OperationFactory.create_operation(
            operation
        )

        result = strategy.execute(
            operand1,
            operand2
        )

        self.history.add_record(
            operation,
            operand1,
            operand2,
            result,
        )

        if len(self.history.history) > self.config.max_history:
            self.history.history = (
                self.history.history
                .tail(self.config.max_history)
                .reset_index(drop=True)
            )

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
        self._notify_observers()

    def undo(self):
        """Undo the most recent change."""
        current_state = self._get_state()

        previous_state = self.memento_manager.undo(
            current_state
        )

        self._restore_state(previous_state)
        self._notify_observers()

        return self.get_history()

    def redo(self):
        """Redo the most recently undone change."""
        current_state = self._get_state()

        next_state = self.memento_manager.redo(
            current_state
        )

        self._restore_state(next_state)
        self._notify_observers()

        return self.get_history()

    def save(self):
        """Manually save history."""
        self.history.save()

    def load(self):
        """Manually load history."""
        return self.history.load()