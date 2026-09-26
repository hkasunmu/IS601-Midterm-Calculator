# Python Command-Line Calculator

## Overview

This project is a modular command-line calculator application built in Python. It supports basic arithmetic operations and uses object-oriented programming, error handling, calculation history, automated testing, and GitHub Actions.

## Features

- Addition
- Subtraction
- Multiplication
- Division
- Calculation history
- Help command
- Exit command
- Input validation
- Division-by-zero error handling
- CalculationFactory design
- REPL command-line interface
- Parameterized testing with pytest
- 100% test coverage
- Automated testing with GitHub Actions

## Project Structure

```text
calculator-assignment/
├── app/
│   ├── calculation/
│   │   ├── __init__.py
│   │   └── calculation.py
│   ├── calculator/
│   │   ├── __init__.py
│   │   ├── calculator.py
│   │   └── repl.py
│   ├── operation/
│   │   ├── __init__.py
│   │   └── operations.py
│   └── __init__.py
├── tests/
│   ├── test_calculations.py
│   ├── test_operations.py
│   └── test_repl.py
├── .github/
│   └── workflows/
│       └── python-app.yml
├── .gitignore
├── README.md
└── requirements.txt