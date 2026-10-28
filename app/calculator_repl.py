
import sys

from app.calculator import Calculator
from app.exceptions import CalculatorError


def colored(text, color_code):
    """Add color when the terminal supports it."""
    if sys.stdout.isatty():
        return f"\033[{color_code}m{text}\033[0m"
    return text


class CalculatorREPL:
    """Command-line interface for the advanced calculator."""

    OPERATIONS = {
        "add",
        "subtract",
        "multiply",
        "divide",
        "power",
        "root",
        "modulus",
        "int_divide",
        "percent",
        "abs_diff",
    }

    def __init__(self, calculator=None):
        self.calculator = (
            calculator if calculator is not None
            else Calculator()
        )

    def show_help(self):
        """Display all supported calculator commands."""
        print("\nAvailable Commands:")

        for operation in sorted(self.OPERATIONS):
            print(f"  {operation} NUMBER NUMBER")

        for command in (
            "history",
            "clear",
            "undo",
            "redo",
            "save",
            "load",
            "help",
            "exit",
        ):
            print(f"  {command}")

        print()

    def show_history(self):
        """Display calculation history."""
        history = self.calculator.get_history()

        if history.empty:
            print("History is empty.")
        else:
            print(history.to_string(index=False))

    def _log_error(self, error):
        """Write calculator errors to the log."""
        logger = getattr(
            self.calculator, "logger", None
        )

        if logger is not None:
            logger.error(
                "Calculator error: %s", error
            )

    def process_command(self, user_input):
        """Process one command entered by the user."""

        user_input = user_input.strip()

        if not user_input:
            return True

        parts = user_input.split()
        command = parts[0].lower()

        try:
            if command == "exit":
                print("Goodbye!")
                return False

            if command == "help":
                self.show_help()
                return True

            if command == "history":
                self.show_history()
                return True

            if command == "clear":
                self.calculator.clear()
                print("History cleared.")
                return True

            if command == "undo":
                self.calculator.undo()
                print("Undo complete.")
                return True

            if command == "redo":
                self.calculator.redo()
                print("Redo complete.")
                return True

            if command == "save":
                self.calculator.save()
                print("History saved.")
                return True

            if command == "load":
                self.calculator.load()
                print("History loaded.")
                return True

            if command in self.OPERATIONS:
                if len(parts) != 3:
                    print(
                        f"Usage: {command} NUMBER NUMBER"
                    )
                    return True

                result = self.calculator.calculate(
                    command,
                    parts[1],
                    parts[2],
                )

                print(
                    colored(
                        f"Result: {result}",
                        "92"
                    )
                )
                return True

            print(
                "Unknown command. Type 'help' "
                "to see available commands."
            )

        except CalculatorError as error:
            self._log_error(error)

            print(
                colored(
                    f"Error: {error}",
                    "91"
                )
            )

        return True

    def run(self):
        """Run the interactive calculator."""

        print("=" * 40)
        print("Enhanced Python Calculator")
        print("=" * 40)
        print("Type 'help' to see available commands.")

        running = True

        while running:
            try:
                user_input = input("calculator> ")

                running = self.process_command(
                    user_input
                )

            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                break

            except CalculatorError as error:
                self._log_error(error)

                print(
                    colored(
                        f"Error: {error}",
                        "91"
                    )
                )


if __name__ == "__main__":  # pragma: no cover
    CalculatorREPL().run()
