from unittest.mock import Mock
import pandas as pd

from app.calculator_repl import CalculatorREPL
from app.exceptions import InvalidInputError


def test_help_command(capsys):
    repl = CalculatorREPL(Mock())

    result = repl.process_command("help")

    output = capsys.readouterr().out

    assert result is True
    assert "Available Commands" in output
    assert "add NUMBER NUMBER" in output


def test_exit_command(capsys):
    repl = CalculatorREPL(Mock())

    result = repl.process_command("exit")

    output = capsys.readouterr().out

    assert result is False
    assert "Goodbye!" in output


def test_empty_command():
    repl = CalculatorREPL(Mock())

    result = repl.process_command("")

    assert result is True


def test_add_command(capsys):
    calculator = Mock()
    calculator.calculate.return_value = 15.0

    repl = CalculatorREPL(calculator)

    result = repl.process_command("add 10 5")

    output = capsys.readouterr().out

    calculator.calculate.assert_called_once_with(
        "add",
        "10",
        "5",
    )

    assert result is True
    assert "Result: 15.0" in output


def test_missing_arguments(capsys):
    repl = CalculatorREPL(Mock())

    result = repl.process_command("add 10")

    output = capsys.readouterr().out

    assert result is True
    assert "Usage: add NUMBER NUMBER" in output


def test_empty_history(capsys):
    calculator = Mock()
    calculator.get_history.return_value.empty = True

    repl = CalculatorREPL(calculator)

    repl.process_command("history")

    output = capsys.readouterr().out

    assert "History is empty." in output


def test_clear_command(capsys):
    calculator = Mock()
    repl = CalculatorREPL(calculator)

    repl.process_command("clear")

    calculator.clear.assert_called_once()
    assert "History cleared." in capsys.readouterr().out


def test_undo_command(capsys):
    calculator = Mock()
    repl = CalculatorREPL(calculator)

    repl.process_command("undo")

    calculator.undo.assert_called_once()
    assert "Undo complete." in capsys.readouterr().out


def test_redo_command(capsys):
    calculator = Mock()
    repl = CalculatorREPL(calculator)

    repl.process_command("redo")

    calculator.redo.assert_called_once()
    assert "Redo complete." in capsys.readouterr().out


def test_save_command(capsys):
    calculator = Mock()
    repl = CalculatorREPL(calculator)

    repl.process_command("save")

    calculator.save.assert_called_once()
    assert "History saved." in capsys.readouterr().out


def test_load_command(capsys):
    calculator = Mock()
    repl = CalculatorREPL(calculator)

    repl.process_command("load")

    calculator.load.assert_called_once()
    assert "History loaded." in capsys.readouterr().out


def test_unknown_command(capsys):
    repl = CalculatorREPL(Mock())

    result = repl.process_command("banana")

    output = capsys.readouterr().out

    assert result is True
    assert "Unknown command" in output
    import pandas as pd

from app.exceptions import InvalidInputError


def test_history_with_records(capsys):
    calculator = Mock()

    calculator.get_history.return_value = pd.DataFrame(
        [
            {
                "operation": "add",
                "operand1": 10,
                "operand2": 5,
                "result": 15,
            }
        ]
    )

    repl = CalculatorREPL(calculator)

    repl.process_command("history")

    output = capsys.readouterr().out

    assert "add" in output
    assert "15" in output


def test_calculator_error(capsys):
    calculator = Mock()

    calculator.calculate.side_effect = InvalidInputError(
        "Invalid number"
    )

    repl = CalculatorREPL(calculator)

    result = repl.process_command(
        "add hello 5"
    )

    output = capsys.readouterr().out

    assert result is True
    assert "Error: Invalid number" in output


def test_run_exit(monkeypatch, capsys):
    repl = CalculatorREPL(Mock())

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: "exit"
    )

    repl.run()

    output = capsys.readouterr().out

    assert "Enhanced Python Calculator" in output
    assert "Goodbye!" in output


def test_run_keyboard_interrupt(
    monkeypatch,
    capsys
):
    repl = CalculatorREPL(Mock())

    def fake_input(prompt):
        raise KeyboardInterrupt

    monkeypatch.setattr(
        "builtins.input",
        fake_input
    )

    repl.run()

    output = capsys.readouterr().out

    assert "Goodbye!" in output