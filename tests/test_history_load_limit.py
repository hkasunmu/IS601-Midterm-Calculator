"""Regression coverage for limiting CSV history at load time."""

from app.calculator import Calculator
from app.history import CalculationHistory


def _create_four_record_csv(path):
    history = CalculationHistory(path)
    for value in (1, 2, 3, 4):
        history.add_record("add", value, 10, value + 10)
    history.save()


def _assert_newest_two(calculator):
    records = calculator.get_history()
    objects = calculator.history.get_calculations()
    assert len(records) == len(objects) == 2
    assert list(records["operand1"]) == [3, 4]
    assert [obj.a for obj in objects] == [3.0, 4.0]
    assert [obj.perform() for obj in objects] == [13, 14]


def test_startup_load_respects_history_limit_in_both_views(tmp_path, monkeypatch):
    """On startup, a four-row CSV must be limited to its newest two rows."""
    path = tmp_path / "saved_history.csv"
    _create_four_record_csv(path)
    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", str(path))
    monkeypatch.setenv("CALCULATOR_LOG_FILE", str(tmp_path / "calculator.log"))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "2")

    calculator = Calculator()
    _assert_newest_two(calculator)


def test_explicit_load_respects_history_limit_in_both_views(tmp_path, monkeypatch):
    """Reloading CSV from the REPL/API also enforces the limit."""
    path = tmp_path / "saved_history.csv"
    _create_four_record_csv(path)
    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", str(path))
    monkeypatch.setenv("CALCULATOR_LOG_FILE", str(tmp_path / "calculator.log"))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "2")

    calculator = Calculator()
    calculator.clear()
    assert calculator.get_history().empty
    result = calculator.load()

    assert len(result) == 2
    _assert_newest_two(calculator)
