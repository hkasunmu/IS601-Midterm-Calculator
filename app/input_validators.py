from app.exceptions import InvalidInputError, InvalidOperationError


def validate_number(value):
    """Convert user input into a number."""
    try:
        return float(value)
    except (ValueError, TypeError):
        raise InvalidInputError(f"Invalid number: {value}")


def validate_operation(operation):
    """Check that the requested calculator operation is valid."""
    valid_operations = {
        "add",
        "subtract",
        "multiply",
        "divide",
        "power",
        "root",
    }

    operation = operation.lower().strip()

    if operation not in valid_operations:
        raise InvalidOperationError(
            f"Invalid operation: {operation}"
        )

    return operation