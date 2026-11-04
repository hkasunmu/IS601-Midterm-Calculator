# IS601 Midterm — Enhanced Python Calculator

A Python command-line calculator with ten operations, an interactive REPL, persistent calculation history, Undo/Redo, configurable validation, event logging, and automated tests. This project extends the earlier calculator assignment and demonstrates the Factory, Memento, and Observer design patterns.

## Features

- **Ten operations** selected through an operation factory.
- **REPL commands:** calculations, `history`, `clear`, `undo`, `redo`, `save`, `load`, `help`, `exit`.
- **CSV persistence** using pandas with operation, operands, result, and UTC timestamp columns. Loading restores actual `Calculation` objects in addition to the DataFrame representation. Legacy CSVs without a timestamp column can still be read.
- **State synchronization:** newly added, restored, undone, redone, cleared, and trimmed records are represented consistently as DataFrame rows and `Calculation` objects.
- **Configuration** through a local `.env` file, with validated settings for input magnitude, decimal precision, history limit, CSV encoding, autosave, and log paths.
- **Errors:** invalid input and division-by-zero errors are reported clearly. Failed calculations do not modify history. A corrupt saved CSV is logged and discarded at startup; invalid startup configuration is reported without an unhandled traceback.
- **Observer pattern:** optional autosaving and event logging using Python's `logging` module.
- **Optional advanced feature:** green calculation results and red errors in ANSI-compatible terminals, with plain-text output when color is not supported.
- **Quality assurance:** `pytest`, `pytest-cov`, and GitHub Actions requiring **at least 90% code coverage**.

## Operation reference

All mathematical commands accept exactly two numbers: `COMMAND NUMBER NUMBER`.

| Command | Description | Example | Typical result |
| --- | --- | --- | --- |
| `add` | Addition | `add 10 5` | `15.0` |
| `subtract` | Subtraction | `subtract 10 5` | `5.0` |
| `multiply` | Multiplication | `multiply 10 5` | `50.0` |
| `divide` | Division | `divide 10 4` | `2.5` |
| `power` | Raise the first number to the second | `power 2 3` | `8.0` |
| `root` | Take the second-number-th root of the first | `root 16 2` | `4.0` |
| `modulus` | Remainder of division | `modulus 10 3` | `1.0` |
| `int_divide` | Quotient truncated toward zero | `int_divide 10 3` | `3` |
| `percent` | `(first / second) * 100` | `percent 25 100` | `25.0` |
| `abs_diff` | Absolute difference | `abs_diff 3 10` | `7.0` |

Division-like commands reject zero denominators. An even root of a negative number is rejected; complex or non-finite calculation results are not added to history. The configured precision can change the displayed numeric result.

## Installation

Requires Python **3.13** (the version used in GitHub Actions) and Git. Other recent Python 3 versions may work but are not the CI target.

```powershell
git clone https://github.com/hkasunmu/IS601-Midterm-Calculator.git
cd IS601-Midterm-Calculator
py -m venv venv
.\venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

On macOS/Linux, use `python3 -m venv venv`, `source venv/bin/activate`, and `python -m pip install -r requirements.txt`.

## Configure `.env`

The environment file is optional. Create `.env` in the repository root, or copy the provided `.env.example` and adjust paths/values. The `.env` file is gitignored.

```dotenv
CALCULATOR_LOG_DIR=logs
CALCULATOR_LOG_FILE=logs/calculator.log
CALCULATOR_HISTORY_DIR=.
CALCULATOR_HISTORY_FILE=calculation_history.csv
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=1000000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

| Variable | Purpose | Default |
| --- | --- | --- |
| `CALCULATOR_LOG_DIR` | Base folder for log files | `logs` |
| `CALCULATOR_LOG_FILE` | Full log file path | `logs/calculator.log` |
| `CALCULATOR_HISTORY_DIR` | Directory used for the default history filename | `.` |
| `CALCULATOR_HISTORY_FILE` | Overrides the history CSV path | `calculation_history.csv` |
| `CALCULATOR_MAX_HISTORY_SIZE` | Number of retained history records (legacy name `CALCULATOR_MAX_HISTORY` is supported) | `100` |
| `CALCULATOR_AUTO_SAVE` | Save after history-changing commands | `true` |
| `CALCULATOR_PRECISION` | Digits after the decimal point, from 0–15 | `2` |
| `CALCULATOR_MAX_INPUT_VALUE` | Maximum absolute value of each operand | `1000000000` |
| `CALCULATOR_DEFAULT_ENCODING` | Encoding for **CSV** save/load | `utf-8` |

`CALCULATOR_HISTORY_FILE` takes priority over `CALCULATOR_HISTORY_DIR`. Invalid numeric precision, history limit, input limit, and unknown encodings raise a `ConfigurationError`. CSV persistence uses the configured encoding in both directions; calculator log files use UTF-8.

## Run the calculator

```powershell
py -m app.calculator_repl
```

Example session:

```text
Enhanced Python Calculator
Type 'help' to see available commands.
calculator> add 10 5
Result: 15.0
calculator> percent 25 100
Result: 25.0
calculator> history
... calculation records and timestamps ...
calculator> undo
Undo complete.
calculator> redo
Redo complete.
calculator> save
History saved.
calculator> load
History loaded.
calculator> exit
Goodbye!
```

Other supported commands:

- `help`: print every operation and command.
- `clear`: remove history (undoable).
- `history`: show calculation rows, including timestamps.
- `undo`, `redo`: restore previous/undone history states with timestamps retained.
- `save`, `load`: manually write/read the configured CSV file.
- `exit`: close the program. Ctrl+C and EOF also exit gracefully.

Errors such as `divide 10 0` display a readable message (red in supported terminals) and allow the next command. Invalid startup settings produce a concise `Unable to start calculator: ...` message instead of a traceback.

## CSV history and `Calculation` objects

The `CalculationHistory` class keeps a pandas DataFrame for display and serialization and a matching list of `Calculation` instances for object-based calculations.

Each CSV row contains:

```text
operation,operand1,operand2,result,timestamp
add,10,5,15,2026-11-04T12:00:00+00:00
```

`load()` reads the configured CSV encoding, validates required columns, and builds `Calculation` objects using `Calculation.from_record()`. `add_record()`, `trim()`, `clear()`, Undo, and Redo keep the two representations synchronized. Missing history files start with empty history. Malformed CSV files raise `HistoryError` on explicit load; at initial startup the error is logged and the calculator starts with empty history.

## Architecture and design patterns

- **Factory:** `app/operations.py` creates strategy operation instances. `app/calculation/calculation.py` also restores/creates the corresponding `Calculation` objects.
- **Memento:** `app/calculator_memento.py` keeps independent Undo/Redo snapshots.
- **Observer:** `AutoSaveObserver` and `LoggingObserver` respond to history-changing events.
- **Facade:** `Calculator` coordinates configuration, arithmetic, history, validation, and observers.
- **REPL:** `app/calculator_repl.py` parses interactive commands and displays errors/results.

Runtime log files live in the configured log directory and are excluded from Git. The application records calculations and input/arithmetic errors at appropriate log levels. See `app/calculator_logger.py` for logging setup.

## Test the project

From the repository root, with the virtual environment activated:

```powershell
py -m pytest -q
py -m pytest --cov=app --cov-report=term-missing --cov-fail-under=90
```

Tests cover operations, factory behavior, REPL commands, logging, configuration, history, Undo/Redo, and corner cases. Additional regression tests verify **all ten operations restored as objects from CSV**, non-default UTF-16 encoding, malformed CSV rejection, object/DataFrame synchronization after history changes, startup error reporting, and REPL continuation after arithmetic errors.

## GitHub Actions and source control

Workflow: [`.github/workflows/python-app.yml`](.github/workflows/python-app.yml). It runs on pushes and pull requests to `main`, sets up Python 3.13, installs `requirements.txt`, executes `pytest`, and fails if coverage is below 90%.

See the repository [Actions tab](https://github.com/hkasunmu/IS601-Midterm-Calculator/actions) for current workflow results. Development and corrections are recorded in Git commit history.

## Repository structure

```text
IS601-Midterm-Calculator/
├── .github/workflows/python-app.yml
├── .env.example
├── app/
│   ├── calculation/calculation.py
│   ├── calculator.py
│   ├── calculator_config.py
│   ├── calculator_logger.py
│   ├── calculator_memento.py
│   ├── calculator_repl.py
│   ├── exceptions.py
│   ├── history.py
│   ├── input_validators.py
│   └── operations.py
├── tests/
├── .gitignore
├── README.md
└── requirements.txt
```

**Repository:** https://github.com/hkasunmu/IS601-Midterm-Calculator
