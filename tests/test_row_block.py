import pytest

from ringing import Row, Change, RowBlock


def test_constructor_bad_input_types() -> None:
    with pytest.raises(TypeError):
        RowBlock('str')
    with pytest.raises(TypeError):
        RowBlock(['str'])
    with pytest.raises(TypeError):
        RowBlock([], [])


def test_changes_not_directly_mutable() -> None:
    changes_in = [Change(5, pn) for pn in ['3', '1', '5']]
    rb = RowBlock(changes_in)

    # Make a local reference to rb.changes, and modify it...
    changes_out = rb.changes
    changes_out.pop()

    # ... then make sure the original hasn't changed
    assert len(changes_in) == 3
    assert len(rb.changes) == 3
    assert rb.changes == changes_in


def test_set_changes() -> None:
    rb = RowBlock([Change(5, pn) for pn in ['3', '1', '5']], '54321')

    new_changes = [Change(5, pn) for pn in ['5', '3']]
    rb.changes = new_changes

    assert rb.changes == new_changes
    assert rb.size == 3
    assert list(rb) == ['54321', '45231', '54213']


def test_set_changes_exceptions() -> None:
    rb = RowBlock([])

    def assign_changes(changes):
        rb.changes = changes

    with pytest.raises(TypeError):
        assign_changes('str')
    with pytest.raises(TypeError):
        assign_changes(['str'])


def test_subscript_bounds() -> None:
    rb = RowBlock([Change(5, pn) for pn in ['3', '1', '5']])

    with pytest.raises(IndexError):
        rb[-1]
    assert rb[0] == '12345'
    assert rb[3] == '32415'
    with pytest.raises(IndexError):
        rb[4]

    with pytest.raises(IndexError):
        rb.__setitem__(-1, Row(5))
    rb[0] = Row(5)
    rb[3] = Row(5)
    with pytest.raises(IndexError):
        rb.__setitem__(4, Row(5))


def test_recalculate_bounds() -> None:
    rb = RowBlock([Change(5, pn) for pn in ['3', '1', '5']])

    with pytest.raises(IndexError):
        rb.recalculate(-1)
    rb.recalculate(0)
    rb.recalculate(3)
    with pytest.raises(IndexError):
        rb.recalculate(4)


def test_iterator() -> None:
    rb = RowBlock([Change(5, pn) for pn in ['3', '1', '5']])

    assert list(rb) == ['12345', '21354', '23145', '32415']
