
from app.calculator import Calculator


def test_calculation_is_logged(tmp_path, monkeypatch):
    log_file = tmp_path / "logs" / "calculator.log"
    history_file = tmp_path / "history.csv"

    monkeypatch.setenv("CALCULATOR_LOG_FILE", str(log_file))
    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", str(history_file))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")

    calculator = Calculator()
    result = calculator.calculate("add", 10, 5)

    assert result == 15.0
    assert log_file.exists()

    content = log_file.read_text(encoding="utf-8")

    assert "Calculation: add 10.0, 5.0 = 15.0" in content


def test_clear_history_is_logged(tmp_path, monkeypatch):
    log_file = tmp_path / "logs" / "calculator.log"
    history_file = tmp_path / "history.csv"

    monkeypatch.setenv("CALCULATOR_LOG_FILE", str(log_file))
    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", str(history_file))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")

    calculator = Calculator()

    calculator.calculate("add", 10, 5)
    calculator.clear()

    content = log_file.read_text(encoding="utf-8")

    assert "History cleared" in content
