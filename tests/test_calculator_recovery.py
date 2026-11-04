import pytest

from app.calculator import Calculator
from app.exceptions import InvalidOperationError


def test_corrupted_csv_does_not_crash_startup(tmp_path, monkeypatch):
    history_file = tmp_path / "broken.csv"
    history_file.write_text("wrong_column\nbad_value\n", encoding="utf-8")
    log_file = tmp_path / "logs" / "calculator.log"

    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", str(history_file))
    monkeypatch.setenv("CALCULATOR_LOG_FILE", str(log_file))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")

    calculator = Calculator()
    assert calculator.get_history().empty
    assert calculator.calculate("add", 2, 3) == 5.0
    assert "Could not load history" in log_file.read_text(encoding="utf-8")


def test_complex_arithmetic_reports_calculator_error(tmp_path, monkeypatch):
    monkeypatch.setenv(
        "CALCULATOR_HISTORY_FILE", str(tmp_path / "history.csv")
    )
    monkeypatch.setenv(
        "CALCULATOR_LOG_FILE", str(tmp_path / "calculator.log")
    )
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")

    calculator = Calculator()
    with pytest.raises(InvalidOperationError):
        calculator.calculate("power", -4, 0.5)

    assert calculator.get_history().empty
    assert calculator.calculate("add", 2, 3) == 5.0


def test_arithmetic_overflow_reports_calculator_error(tmp_path, monkeypatch):
    monkeypatch.setenv(
        "CALCULATOR_HISTORY_FILE", str(tmp_path / "history.csv")
    )
    monkeypatch.setenv(
        "CALCULATOR_LOG_FILE", str(tmp_path / "calculator.log")
    )
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")

    calculator = Calculator()
    with pytest.raises(InvalidOperationError):
        calculator.calculate("power", 1_000_000_000, 1_000_000_000)
    assert calculator.get_history().empty
