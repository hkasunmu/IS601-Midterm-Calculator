import pandas as pd
import pytest

from app.exceptions import HistoryError
from app.history import CalculationHistory


def test_history_starts_empty(tmp_path):
    filename = tmp_path / "history.csv"

    history = CalculationHistory(filename)

    assert history.get_history().empty


def test_add_record(tmp_path):
    filename = tmp_path / "history.csv"

    history = CalculationHistory(filename)

    history.add_record(
        "add",
        10,
        5,
        15
    )

    result = history.get_history()

    assert len(result) == 1
    assert result.iloc[0]["operation"] == "add"
    assert result.iloc[0]["operand1"] == 10
    assert result.iloc[0]["operand2"] == 5
    assert result.iloc[0]["result"] == 15


def test_clear_history(tmp_path):
    filename = tmp_path / "history.csv"

    history = CalculationHistory(filename)

    history.add_record(
        "multiply",
        4,
        3,
        12
    )

    history.clear()

    assert history.get_history().empty


def test_save_history(tmp_path):
    filename = tmp_path / "history.csv"

    history = CalculationHistory(filename)

    history.add_record(
        "add",
        10,
        5,
        15
    )

    history.save()

    assert filename.exists()


def test_load_history(tmp_path):
    filename = tmp_path / "history.csv"

    original = CalculationHistory(filename)

    original.add_record(
        "subtract",
        10,
        4,
        6
    )

    original.save()

    loaded = CalculationHistory(filename)

    result = loaded.load()

    assert len(result) == 1
    assert result.iloc[0]["operation"] == "subtract"
    assert result.iloc[0]["result"] == 6


def test_load_missing_file_returns_empty_history(tmp_path):
    filename = tmp_path / "missing.csv"

    history = CalculationHistory(filename)

    result = history.load()

    assert result.empty


def test_get_history_returns_copy(tmp_path):
    filename = tmp_path / "history.csv"

    history = CalculationHistory(filename)

    history.add_record(
        "add",
        1,
        2,
        3
    )

    copied_history = history.get_history()

    copied_history.loc[0, "result"] = 999

    assert history.get_history().iloc[0]["result"] == 3


def test_save_error(monkeypatch, tmp_path):
    filename = tmp_path / "history.csv"

    history = CalculationHistory(filename)

    def fake_to_csv(*args, **kwargs):
        raise OSError("Save failed")

    monkeypatch.setattr(
        pd.DataFrame,
        "to_csv",
        fake_to_csv
    )

    with pytest.raises(HistoryError):
        history.save()


def test_load_error(monkeypatch, tmp_path):
    filename = tmp_path / "history.csv"

    filename.write_text("test")

    history = CalculationHistory(filename)

    def fake_read_csv(*args, **kwargs):
        raise OSError("Load failed")

    monkeypatch.setattr(
        pd,
        "read_csv",
        fake_read_csv
    )

    with pytest.raises(HistoryError):
        history.load()