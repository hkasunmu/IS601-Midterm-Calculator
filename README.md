IS601 Midterm – Enhanced Python Calculator
An advanced, command-line calculator built in Python for the IS601 midterm project. This project extends an earlier calculator with additional arithmetic operations, calculation history, undo/redo, logging, configurable settings, automated tests, and continuous integration (CI).
Features
- Ten arithmetic operations, implemented through an operation factory.
- Interactive read-eval-print loop (REPL) with help, history, clear, undo, redo, save, load, and exit commands.
- Calculation history stored as pandas data and saved to/loaded from CSV. Each saved row contains a timestamp, and loading reconstructs Calculation objects through Calculation.from_record(). Older CSV files without timestamps are supported.
- Undo/redo using the Memento pattern.
- Automatic history saving and calculation event logging using observers.
- Custom exceptions and validation for invalid numbers, unsupported operations, division by zero, complex/nonfinite arithmetic results, overflow, and excessively large inputs. A malformed history CSV is logged and does not prevent the calculator from starting.
- Environment-based configuration through a .env file.
- Optional advanced feature: color-coded results (green) and errors (red) in compatible terminals.
- Automated testing with pytest and pytest-cov; GitHub Actions runs the tests and enforces a minimum 90% coverage threshold.
Mathematical operations
Each mathematical command takes two numbers:
Command	Description	Example	Expected result
add	Addition	add 10 5	15.0
subtract	Subtraction	subtract 10 5	5.0
multiply	Multiplication	multiply 10 5	50.0
divide	Division	divide 10 4	2.5
power	Exponentiation	power 2 3	8.0
root	Root using a degree	root 27 3	3.0 (approximately)
modulus	Remainder	modulus 10 3	1.0
int_divide	Integer quotient, truncating fractional part	int_divide 10 3	3
percent	(first / second) * 100	percent 25 100	25.0
abs_diff	Absolute difference	abs_diff 3 10	7.0


Division-based commands handle a zero divisor with a meaningful error. Calculation results are rounded according to the configured precision.
Requirements and installation
Use Python 3 and Git. On Windows, these examples use PowerShell and the py launcher.
1. Clone the repository:
   git clone https://github.com/hkasunmu/IS601-Midterm-Calculator.git
   cd IS601-Midterm-Calculator
2. Create and activate a virtual environment:
   py -m venv venv
   .\venv\Scripts\Activate.ps1
   On macOS or Linux, use python3 -m venv venv and source venv/bin/activate instead.
3. Install dependencies:
   py -m pip install -r requirements.txt
4. Configure environment variables if desired, following the next section.
Configuration (.env)
Create a .env file at the project root if one does not already exist. Example settings:
CALCULATOR_LOG_DIR=logs
CALCULATOR_LOG_FILE=logs/calculator.log
CALCULATOR_HISTORY_DIR=.
CALCULATOR_HISTORY_FILE=calculation_history.csv
CALCULATOR_AUTO_SAVE=true
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=1000000000
CALCULATOR_DEFAULT_ENCODING=utf-8
- Log settings: Choose where calculator event/error logs are written.
- History settings: Choose the CSV location, enable or disable automatic saves, and limit retained history.
- Precision: Control the number of decimal places for calculation results.
- Maximum input: Reject values with an absolute magnitude above the configured limit.
- Encoding: CALCULATOR_DEFAULT_ENCODING controls pandas CSV reading and writing, including non-default encodings such as utf-16. Both CalculationHistory and the calculator use this setting.
The application supplies defaults for missing settings. Invalid configuration values are reported using custom configuration errors. The .env file is ignored by Git so local configuration does not get committed.
Run the application
From the project root:
py -m app.calculator_repl
At the calculator> prompt, try:
help
add 10 5
percent 25 100
abs_diff 3 10
history
undo
redo
save
load
clear
exit
The help command lists the available operations. history displays previous calculations. undo reverses the last history change; redo restores an undone change. save writes history to CSV; load reads it back; clear removes current history. exit ends the session. Pressing Ctrl+C also exits gracefully.
History, logging, and error handling
History is managed with a pandas DataFrame. Saved CSV records contain operation, operand1, operand2, result, and timestamp. On load(), records are converted to actual Calculation objects accessible through history.calculations or history.get_calculations(); these can perform their saved mathematical operations. CSV files without a timestamp column remain compatible. Pandas reads and writes CSV using CALCULATOR_DEFAULT_ENCODING. Logs record calculation activity and errors using Python's logging module, with timestamps and severity levels such as INFO, WARNING, and ERROR. Logs are stored in the configured location (by default logs/calculator.log).

The calculator provides error messages for situations such as an unsupported command, invalid numeric input, attempting to divide by zero, complex-number results, overflow, or an input exceeding the configured limit. If CSV history is missing, loading starts with an empty history; if the CSV is malformed or unreadable at startup, the calculator logs a warning and recovers with empty history. Invalid arithmetic operations are reported using calculator exceptions rather than crashing the command loop. With the optional color feature, supported terminals show results in green and errors in red.
Design patterns
- Factory: OperationFactory chooses the mathematical operation from a command name.
- Strategy: Each operation class implements its own execute() behavior.
- Memento: MementoManager stores calculator state for undo/redo.
- Observer: AutoSaveObserver and LoggingObserver respond to calculator changes.
- Facade: Calculator provides a simple interface to configuration, validation, operations, history, and observers.
Testing and coverage
Run the full test suite:
py -m pytest -q
Run tests with a terminal coverage report and enforce the 90% minimum:
py -m pytest --cov=app --cov-report=term-missing --cov-fail-under=90
Tests cover mathematical operations, invalid input, zero division, the REPL, configuration, history persistence, the Memento behavior, and logging. tests/test_history_restoration.py verifies restoration of each of the 10 operations as a Calculation object, non-default UTF-16 CSV encoding, and malformed-file rejection. tests/test_calculator_recovery.py verifies startup recovery from damaged CSV history and safe handling of arithmetic errors or overflow. The coverage report should be rerun after any code changes; a prior local report is not a guarantee for later commits.
Continuous integration (GitHub Actions)
The workflow at .github/workflows/python-app.yml runs automated tests for changes on the main branch and checks code coverage. It is designed to fail when coverage falls below 90%.

Check current workflow results in the repository's Actions tab:

https://github.com/hkasunmu/IS601-Midterm-Calculator/actions
Project layout
IS601-Midterm-Calculator/
├── .github/workflows/python-app.yml
├── app/
│   ├── calculation/
│   │   └── calculation.py
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
│   ├── test_history_restoration.py
│   └── test_calculator_recovery.py
├── .gitignore
├── README.md
└── requirements.txt
Development workflow and version control
Development is tracked through descriptive Git commits on main, with the corrective work recorded in separate commits for CSV restoration, startup/arithmetic error recovery, and documentation. Verify that GitHub Actions has a green check on the latest commit before submitting.
Repository
https://github.com/hkasunmu/IS601-Midterm-Calculator