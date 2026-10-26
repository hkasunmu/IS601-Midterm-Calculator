from app.operations import OperationFactory


def test_absolute_difference():
    operation = OperationFactory.create_operation("abs_diff")
    assert operation.execute(10, 3) == 7


def test_absolute_difference_reversed():
    operation = OperationFactory.create_operation("abs_diff")
    assert operation.execute(3, 10) == 7


def test_absolute_difference_negative():
    operation = OperationFactory.create_operation("abs_diff")
    assert operation.execute(-5, 10) == 15


def test_absolute_difference_same_numbers():
    operation = OperationFactory.create_operation("abs_diff")
    assert operation.execute(5, 5) == 0