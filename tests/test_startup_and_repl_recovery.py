"""Exercise startup errors and recovering from invalid arithmetic in the REPL."""
import os
from pathlib import Path
import subprocess
import sys

from app.calculator_repl import CalculatorREPL


def test_invalid_startup_precision_is_explained_without_traceback(tmp_path):
    environment = os.environ.copy()
    environment["CALCULATOR_PRECISION"] = "invalid"
    environment["CALCULATOR_HISTORY_FILE"] = str(tmp_path / "history.csv")
    environment["CALCULATOR_LOG_FILE"] = str(tmp_path / "calculator.log")

    completed = subprocess.run(
        [sys.executable, "-m", "app.calculator_repl"],
        cwd=Path(__file__).resolve().parents[1],
        env=environment,
        text=True,
        capture_output=True,
        timeout=10,
        check=False,
    )

    assert completed.returncode == 1
    assert "Unable to start calculator:" in completed.stderr
    assert "CALCULATOR_PRECISION" in completed.stderr
    assert "Traceback" not in completed.stderr


def test_unusable_log_path_is_explained_without_traceback(tmp_path):
    existing_file = tmp_path / "not_a_directory"
    existing_file.write_text("not a directory", encoding="utf-8")
    environment = os.environ.copy()
    environment["CALCULATOR_PRECISION"] = "2"
    environment["CALCULATOR_LOG_FILE"] = str(existing_file / "calculator.log")

    completed = subprocess.run(
        [sys.executable, "-m", "app.calculator_repl"],
        cwd=Path(__file__).resolve().parents[1],
        env=environment,
        text=True,
        capture_output=True,
        timeout=10,
        check=False,
    )

    assert completed.returncode == 1
    assert "Unable to start calculator:" in completed.stderr
    assert "Traceback" not in completed.stderr


def test_repl_continues_after_division_by_zero(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("CALCULATOR_HISTORY_FILE", str(tmp_path / "history.csv"))
    monkeypatch.setenv("CALCULATOR_LOG_FILE", str(tmp_path / "calculator.log"))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    from app.calculator import Calculator

    commands = iter(["divide 10 0", "add 2 3", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(commands))
    CalculatorREPL(Calculator()).run()
    output = capsys.readouterr().out
    assert "Cannot divide by zero" in output
    assert "Result: 5.0" in output
    assert "Goodbye!" in output
