import pytest

from app.calculator import Calculator, CalculatorObserver
from app.exceptions import InvalidInputError


@pytest.fixture
def calculator(tmp_path, monkeypatch):
    history_file = tmp_path / "test_history.csv"

    monkeypatch.setenv(
        "CALCULATOR_HISTORY_FILE",
        str(history_file)
    )

    monkeypatch.setenv(
        "CALCULATOR_AUTO_SAVE",
        "false"
    )

    monkeypatch.setenv(
        "CALCULATOR_MAX_HISTORY",
        "3"
    )

    return Calculator()


@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        ("add", 10, 5, 15),
        ("subtract", 10, 5, 5),
        ("multiply", 10, 5, 50),
        ("divide", 10, 5, 2),
        ("power", 2, 3, 8),
        ("root", 16, 2, 4),
    ],
)
def test_calculate(calculator, operation, a, b, expected):
    result = calculator.calculate(
        operation,
        a,
        b
    )

    assert result == pytest.approx(expected)


def test_calculation_added_to_history(calculator):
    calculator.calculate("add", 10, 5)

    history = calculator.get_history()

    assert len(history) == 1
    assert history.iloc[0]["operation"] == "add"
    assert history.iloc[0]["result"] == 15


def test_invalid_number(calculator):
    with pytest.raises(InvalidInputError):
        calculator.calculate(
            "add",
            "hello",
            5
        )


def test_clear_history(calculator):
    calculator.calculate("add", 10, 5)

    calculator.clear()

    assert calculator.get_history().empty


def test_undo(calculator):
    calculator.calculate("add", 10, 5)
    calculator.calculate("multiply", 4, 3)

    calculator.undo()

    history = calculator.get_history()

    assert len(history) == 1
    assert history.iloc[0]["operation"] == "add"


def test_redo(calculator):
    calculator.calculate("add", 10, 5)
    calculator.calculate("multiply", 4, 3)

    calculator.undo()
    calculator.redo()

    history = calculator.get_history()

    assert len(history) == 2
    assert history.iloc[1]["operation"] == "multiply"


def test_max_history(calculator):
    calculator.calculate("add", 1, 1)
    calculator.calculate("add", 2, 2)
    calculator.calculate("add", 3, 3)
    calculator.calculate("add", 4, 4)

    history = calculator.get_history()

    assert len(history) == 3


def test_manual_save_and_load(
    tmp_path,
    monkeypatch
):
    history_file = tmp_path / "saved.csv"

    monkeypatch.setenv(
        "CALCULATOR_HISTORY_FILE",
        str(history_file)
    )

    monkeypatch.setenv(
        "CALCULATOR_AUTO_SAVE",
        "false"
    )

    calculator = Calculator()

    calculator.calculate("add", 10, 5)
    calculator.save()

    new_calculator = Calculator()

    history = new_calculator.load()

    assert len(history) == 1
    assert history.iloc[0]["result"] == 15


def test_auto_save(
    tmp_path,
    monkeypatch
):
    history_file = tmp_path / "autosave.csv"

    monkeypatch.setenv(
        "CALCULATOR_HISTORY_FILE",
        str(history_file)
    )

    monkeypatch.setenv(
        "CALCULATOR_AUTO_SAVE",
        "true"
    )

    calculator = Calculator()

    calculator.calculate("add", 10, 5)

    assert history_file.exists()


class DummyObserver(CalculatorObserver):
    def __init__(self):
        self.called = False

    def update(self, calculator):
        self.called = True


def test_add_observer(calculator):
    observer = DummyObserver()

    calculator.add_observer(observer)

    calculator.calculate("add", 2, 3)

    assert observer.called is True