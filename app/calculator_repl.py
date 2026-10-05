from app.calculator import Calculator
from app.exceptions import CalculatorError

class CalculatorREPL:
    """Command-line interface for the calculator."""

    OPERATIONS = {
        "add",
        "subtract",
        "multiply",
        "divide",
        "power",
        "root",
    }

    def __init__(self, calculator=None):
        self.calculator = calculator or Calculator()

    def show_help(self):
        """Display available calculator commands."""
        print("\nAvailable Commands:")
        print("  add NUMBER NUMBER")
        print("  subtract NUMBER NUMBER")
        print("  multiply NUMBER NUMBER")
        print("  divide NUMBER NUMBER")
        print("  power NUMBER NUMBER")
        print("  root NUMBER NUMBER")
        print("  history")
        print("  clear")
        print("  undo")
        print("  redo")
        print("  save")
        print("  load")
        print("  help")
        print("  exit\n")

    def show_history(self):
        """Display calculation history."""
        history = self.calculator.get_history()

        if history.empty:
            print("History is empty.")
        else:
            print(history.to_string(index=False))

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

                print(f"Result: {result}")
                return True

            print(
                "Unknown command. Type 'help' "
                "to see available commands."
            )

        except CalculatorError as error:
            print(f"Error: {error}")

        return True

    def run(self):
        """Start the calculator REPL."""
        print("=" * 40)
        print("Enhanced Python Calculator")
        print("=" * 40)
        print("Type 'help' to see available commands.")

        running = True

        while running:
            try:
                user_input = input("calculator> ")
                running = self.process_command(user_input)

            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                break
            
            
 
if __name__ == "__main__":  # pragma: no cover
    CalculatorREPL().run()