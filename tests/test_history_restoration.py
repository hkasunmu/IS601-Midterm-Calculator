
import pytest

from app.history import CalculationHistory
from app.calculation.calculation import Calculation
from app.exceptions import HistoryError


@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        ("add", 10, 5, 15),
        ("subtract", 10, 5, 5),
        ("multiply", 5, 3, 15),
        ("divide", 10, 2, 5),
        ("power", 2, 3, 8),
        ("root", 16, 2, 4),
        ("modulus", 10, 3, 1),
        ("int_divide", 10, 3, 3),
        ("percent", 25, 100, 25),
        ("abs_diff", 3, 10, 7),
    ],
)
def test_restore_all_operations(
    tmp_path, operation, a, b, expected
):
    filename = tmp_path / "history.csv"

    history = CalculationHistory(filename)
    history.add_record(
        operation,
        a,
        b,
        expected,
        timestamp="2026-11-04T12:00:00+00:00"
    )
    history.save()

    restored = CalculationHistory(filename)
    restored.load()

    assert len(restored.calculations) == 1

    calculation = restored.calculations[0]

    assert isinstance(calculation, Calculation)
    assert calculation.operation_name == operation
    assert calculation.perform() == pytest.approx(expected)
    assert calculation.result == pytest.approx(expected)
    assert calculation.timestamp == "2026-11-04T12:00:00+00:00"


def test_configured_csv_encoding(tmp_path, monkeypatch):
    monkeypatch.setenv(
        "CALCULATOR_DEFAULT_ENCODING", "utf-16"
    )

    filename = tmp_path / "encoded_history.csv"

    history = CalculationHistory(filename)
    history.add_record("add", 10, 5, 15)
    history.save()

    assert history.encoding == "utf-16"

    text = filename.read_text(encoding="utf-16")
    assert "operation" in text
    assert "timestamp" in text

    restored = CalculationHistory(filename)
    restored.load()

    assert restored.encoding == "utf-16"
    assert len(restored.calculations) == 1
    assert restored.calculations[0].perform() == 15


def test_malformed_csv_raises_history_error(tmp_path):
    filename = tmp_path / "bad_history.csv"
    filename.write_text(
        "invalid_column\nbad_data\n",
        encoding="utf-8"
    )

    history = CalculationHistory(
        filename, encoding="utf-8"
    )

    with pytest.raises(HistoryError):
        history.load()
