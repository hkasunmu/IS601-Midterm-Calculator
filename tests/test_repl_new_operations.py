import pytest
from unittest.mock import Mock

from app.calculator_repl import CalculatorREPL


@pytest.mark.parametrize(
    "command, operation, a, b, expected",
    [
        ("modulus 10 3", "modulus", "10", "3", 1.0),
        ("int_divide 10 3", "int_divide", "10", "3", 3),
        ("percent 25 100", "percent", "25", "100", 25.0),
        ("abs_diff 3 10", "abs_diff", "3", "10", 7.0),
    ],
)
def test_new_repl_operations(
    capsys, command, operation, a, b, expected
):
    calculator = Mock()
    calculator.calculate.return_value = expected

    repl = CalculatorREPL(calculator)
    result = repl.process_command(command)

    calculator.calculate.assert_called_once_with(
        operation, a, b
    )
    assert result is True
    assert f"Result: {expected}" in capsys.readouterr().out


def test_help_shows_new_operations(capsys):
    repl = CalculatorREPL(Mock())
    repl.process_command("help")

    output = capsys.readouterr().out

    for operation in (
        "modulus",
        "int_divide",
        "percent",
        "abs_diff",
    ):
        assert f"{operation} NUMBER NUMBER" in output