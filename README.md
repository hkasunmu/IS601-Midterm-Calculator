# Enhanced Python Calculator

This project is an enhanced command-line calculator built with Python. It was created to demonstrate object-oriented programming, advanced design patterns, pandas data management, error handling, automated testing, and GitHub Actions.

## Features

The calculator supports the following operations:

- Addition
- Subtraction
- Multiplication
- Division
- Power
- Root

It also includes:

- Calculation history
- pandas DataFrame storage
- CSV saving and loading
- Automatic history saving
- Undo and redo
- Input validation
- Error handling
- Environment variable configuration
- REPL command-line interface
- Automated testing with pytest
- 100% test coverage
- GitHub Actions continuous integration

## Design Patterns

This project uses several design patterns.

### Factory Pattern

The `OperationFactory` creates the correct operation object based on the user's command.

### Strategy Pattern

Each mathematical operation is implemented as its own strategy, including addition, subtraction, multiplication, division, power, and root.

### Observer Pattern

Observers react when calculator activity occurs. The `AutoSaveObserver` automatically saves calculation history when enabled.

### Memento Pattern

The Memento pattern stores previous calculator states so the user can undo and redo changes.

### Facade Pattern

The `Calculator` class provides a simple interface that connects the operations, history, configuration, validation, observers, and memento system.

## Project Structure

```text
calculator-assignment/
│
├── app/
│   ├── __init__.py
│   ├── calculator.py
│   ├── calculator_config.py
│   ├── calculator_memento.py
│   ├── calculator_repl.py
│   ├── exceptions.py
│   ├── history.py
│   ├── input_validators.py
│   └── operations.py
│
├── tests/
│   ├── test_calculations.py
│   ├── test_calculator_config.py
│   ├── test_calculator_memento.py
│   ├── test_calculator_repl.py
│   ├── test_exceptions.py
│   ├── test_history.py
│   ├── test_input_validators.py
│   └── test_operations.py
│
├── .github/
│   └── workflows/
│       └── python-app.yml
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt