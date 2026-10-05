from app.calculator_memento import CalculatorMemento, MementoManager


def test_memento_returns_saved_state():
    original_state = [1, 2, 3]

    memento = CalculatorMemento(original_state)

    assert memento.get_state() == [1, 2, 3]


def test_memento_uses_deepcopy():
    original_state = [[1, 2]]

    memento = CalculatorMemento(original_state)

    original_state[0].append(3)

    assert memento.get_state() == [[1, 2]]


def test_save_state_adds_to_undo_stack():
    manager = MementoManager()

    manager.save_state([1])

    assert len(manager.undo_stack) == 1


def test_save_state_clears_redo_stack():
    manager = MementoManager()

    manager.redo_stack.append(
        CalculatorMemento([1])
    )

    manager.save_state([2])

    assert len(manager.redo_stack) == 0


def test_undo_restores_previous_state():
    manager = MementoManager()

    manager.save_state([1, 2])

    result = manager.undo([1, 2, 3])

    assert result == [1, 2]


def test_redo_restores_next_state():
    manager = MementoManager()

    manager.save_state([1, 2])

    manager.undo([1, 2, 3])

    result = manager.redo([1, 2])

    assert result == [1, 2, 3]


def test_undo_with_empty_stack_returns_current_state():
    manager = MementoManager()

    current_state = [1, 2, 3]

    result = manager.undo(current_state)

    assert result == current_state


def test_redo_with_empty_stack_returns_current_state():
    manager = MementoManager()

    current_state = [1, 2, 3]

    result = manager.redo(current_state)

    assert result == current_state