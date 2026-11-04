"""Regression tests for synchronized DataFrame and Calculation-object history."""
import pytest

from app.calculator import Calculator
from app.calculation.calculation import Calculation
from app.history import CalculationHistory


def test_new_record_updates_calculation_objects(tmp_path):
    history = CalculationHistory(tmp_path / "records.csv")
    history.add_record("add", 2, 3, 5, timestamp="2026-11-04T12:00:00+00:00")

    assert len(history.get_history()) == len(history.calculations) == 1
    assert isinstance(history.calculations[0], Calculation)
    assert history.calculations[0].perform() == 5
    assert history.calculations[0].timestamp == "2026-11-04T12:00:00+00:00"


def test_loaded_records_stay_synchronized_when_new_record_added(tmp_path):
    original = CalculationHistory(tmp_path / "records.csv")
    original.add_record("add", 2, 3, 5)
    original.save()

    restored = CalculationHistory(original.filename)
    restored.load()
    restored.add_record("multiply", 4, 3, 12)

    assert len(restored.get_history()) == len(restored.calculations) == 2
    assert [c.operation_name for c in restored.calculations] == ["add", "multiply"]
    assert restored.calculations[-1].perform() == 12
    assert len(restored.get_calculations()) == 2


def test_trim_keeps_object_list_and_dataframe_aligned(tmp_path):
    history = CalculationHistory(tmp_path / "records.csv")
    for value in range(4):
        history.add_record("add", value, 1, value + 1)
    history.trim(2)

    assert list(history.get_history()["operand1"]) == [2, 3]
    assert [c.a for c in history.calculations] == [2.0, 3.0]


def test_undo_redo_and_clear_synchronize_objects(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", str(tmp_path / "history.csv"))
    monkeypatch.setenv("CALCULATOR_LOG_FILE", str(tmp_path / "calculator.log"))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    calculator = Calculator()
    calculator.calculate("add", 2, 3)
    calculator.calculate("abs_diff", 3, 10)

    assert len(calculator.history.calculations) == 2
    calculator.undo()
    assert [c.operation_name for c in calculator.history.calculations] == ["add"]
    calculator.redo()
    assert [c.operation_name for c in calculator.history.calculations] == ["add", "abs_diff"]
    calculator.clear()
    assert calculator.history.calculations == []


def test_calculator_max_history_trims_objects(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", str(tmp_path / "history.csv"))
    monkeypatch.setenv("CALCULATOR_LOG_FILE", str(tmp_path / "calculator.log"))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "2")
    calculator = Calculator()
    for value in (1, 2, 3):
        calculator.calculate("add", value, 1)

    assert len(calculator.history.calculations) == len(calculator.get_history()) == 2
    assert [c.a for c in calculator.history.calculations] == [2.0, 3.0]
