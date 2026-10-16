import pytest

from ringing import Row, Change, RowBlock


class TestRowBlock:
    def test_row_block_constructor_exceptions(self):
        with pytest.raises(TypeError):
            RowBlock(self)
        with pytest.raises(TypeError):
            RowBlock([self])
        with pytest.raises(TypeError):
            RowBlock([], self)

    def test_row_block_changes_not_directly_mutable(self):
        changes_in = [Change(5, pn) for pn in ['3', '1', '5']]
        rb = RowBlock(changes_in)

        # Make a local reference to rb.changes, and modify it...
        changes_out = rb.changes
        changes_out.pop()

        # ... then make sure the original hasn't changed
        assert len(changes_in) == 3
        assert len(rb.changes) == 3
        assert rb.changes == changes_in

    def test_row_block_set_changes(self):
        rb = RowBlock([Change(5, pn) for pn in ['3', '1', '5']], '54321')

        new_changes = [Change(5, pn) for pn in ['5', '3']]
        rb.changes = new_changes

        assert rb.changes == new_changes
        assert rb.size == 3
        assert list(rb) == ['54321', '45231', '54213']

    def test_row_block_set_changes_exceptions(self):
        rb = RowBlock([])

        def assign_changes(changes):
            rb.changes = changes

        with pytest.raises(TypeError):
            assign_changes(self)
        with pytest.raises(TypeError):
            assign_changes([self])

    def test_row_block_subscript_bounds(self):
        rb = RowBlock([Change(5, pn) for pn in ['3', '1', '5']])

        with pytest.raises(IndexError):
            rb[-1]
        assert rb[0] == '12345'
        assert rb[3] == '32415'
        with pytest.raises(IndexError):
            rb[4]

        with pytest.raises(IndexError):
            rb.__setitem__(-1, Row(5))
        rb[0] = Row(5)  # Should succeed
        rb[3] = Row(5)
        with pytest.raises(IndexError):
            rb.__setitem__(4, Row(5))

    def test_row_block_recalculate_bounds(self):
        rb = RowBlock([Change(5, pn) for pn in ['3', '1', '5']])

        with pytest.raises(IndexError):
            rb.recalculate(-1)
        rb.recalculate(0)
        rb.recalculate(3)
        with pytest.raises(IndexError):
            rb.recalculate(4)

    def test_row_block_iterator(self):
        rb = RowBlock([Change(5, pn) for pn in ['3', '1', '5']])

        assert list(rb) == ['12345', '21354', '23145', '32415']
