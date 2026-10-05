from app.calculator.calculator import Calculator


def show_help():
    """Display available calculator commands."""
    print("\nAvailable commands:")
    print("add       - Add two numbers")
    print("subtract  - Subtract two numbers")
    print("multiply  - Multiply two numbers")
    print("divide    - Divide two numbers")
    print("history   - Show calculation history")
    print("help      - Show available commands")
    print("exit      - Exit the calculator")


def run_calculator():
    """Run the calculator REPL."""
    calculator = Calculator()

    print("Welcome to the Python Calculator!")
    print("Type 'help' to see available commands.")

    while True:
        command = input("\nEnter command: ").strip().lower()

        if command == "exit":
            print("Goodbye!")
            break

        if command == "help":
            show_help()
            continue

        if command == "history":
            history = calculator.get_history()

            if not history:
                print("No calculations in history.")
            else:
                print("\nCalculation History:")
                for calculation in history:
                    print(calculation)
            continue

        if command not in ["add", "subtract", "multiply", "divide"]:
            print("Invalid command. Type 'help' for available commands.")
            continue

        try:
            first_number = float(input("Enter first number: "))
            second_number = float(input("Enter second number: "))

            result = calculator.calculate(
                command,
                first_number,
                second_number
            )

            print(f"Result: {result}")

        except ValueError:
            print("Invalid input. Please enter valid numbers.")

        except ZeroDivisionError as error:
            print(f"Error: {error}")


if __name__ == "__main__":  # pragma: no cover
    run_calculator()