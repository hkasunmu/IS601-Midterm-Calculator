import pytest

import app.calculator_config as config_module
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


def test_config_defaults(monkeypatch):
    monkeypatch.setattr(
        config_module,
        "load_dotenv",
        lambda: None
    )

    monkeypatch.delenv(
        "CALCULATOR_HISTORY_FILE",
        raising=False
    )

    monkeypatch.delenv(
        "CALCULATOR_AUTO_SAVE",
        raising=False
    )

    monkeypatch.delenv(
        "CALCULATOR_MAX_HISTORY",
        raising=False
    )

    config = CalculatorConfig()

    assert config.history_file == "calculation_history.csv"
    assert config.auto_save is True
    assert config.max_history == 100


def test_config_custom_values(monkeypatch):
    monkeypatch.setenv(
        "CALCULATOR_HISTORY_FILE",
        "my_history.csv"
    )

    monkeypatch.setenv(
        "CALCULATOR_AUTO_SAVE",
        "false"
    )

    monkeypatch.setenv(
        "CALCULATOR_MAX_HISTORY",
        "50"
    )

    config = CalculatorConfig()

    assert config.history_file == "my_history.csv"
    assert config.auto_save is False
    assert config.max_history == 50


def test_auto_save_true(monkeypatch):
    monkeypatch.setenv(
        "CALCULATOR_AUTO_SAVE",
        "TRUE"
    )

    config = CalculatorConfig()

    assert config.auto_save is True


@pytest.mark.parametrize(
    "value",
    [
        "0",
        "-1",
        "hello",
    ],
)
def test_invalid_max_history(monkeypatch, value):
    monkeypatch.setenv(
        "CALCULATOR_MAX_HISTORY",
        value
    )

    with pytest.raises(ConfigurationError):
        CalculatorConfig()