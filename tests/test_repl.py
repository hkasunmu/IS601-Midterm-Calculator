from app.calculator.repl import show_help, run_calculator


def test_show_help(capsys):
    show_help()
    output = capsys.readouterr().out

    assert "Available commands:" in output
    assert "add" in output
    assert "subtract" in output
    assert "multiply" in output
    assert "divide" in output
    assert "history" in output
    assert "help" in output
    assert "exit" in output


def test_exit(monkeypatch, capsys):
    inputs = iter(["exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    run_calculator()

    output = capsys.readouterr().out
    assert "Welcome to the Python Calculator!" in output
    assert "Goodbye!" in output


def test_help_command(monkeypatch, capsys):
    inputs = iter(["help", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    run_calculator()

    output = capsys.readouterr().out
    assert "Available commands:" in output


def test_empty_history(monkeypatch, capsys):
    inputs = iter(["history", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    run_calculator()

    output = capsys.readouterr().out
    assert "No calculations in history." in output


def test_calculation_and_history(monkeypatch, capsys):
    inputs = iter(["add", "5", "3", "history", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    run_calculator()

    output = capsys.readouterr().out
    assert "Result: 8.0" in output
    assert "Calculation History:" in output


def test_invalid_command(monkeypatch, capsys):
    inputs = iter(["power", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    run_calculator()

    output = capsys.readouterr().out
    assert "Invalid command." in output


def test_invalid_number(monkeypatch, capsys):
    inputs = iter(["add", "abc", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    run_calculator()

    output = capsys.readouterr().out
    assert "Invalid input." in output


def test_division_by_zero(monkeypatch, capsys):
    inputs = iter(["divide", "10", "0", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    run_calculator()

    output = capsys.readouterr().out
    assert "Cannot divide by zero." in output