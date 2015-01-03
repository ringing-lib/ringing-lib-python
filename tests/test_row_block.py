import unittest

from ringing import Row, Change, RowBlock


class RowBlockTest(unittest.TestCase):
    def test_row_block_constructor_exceptions(self):
        self.assertRaises(TypeError, lambda: RowBlock(self))
        self.assertRaises(TypeError, lambda: RowBlock([self]))
        self.assertRaises(TypeError, lambda: RowBlock([], self))

    def test_row_block_changes_not_directly_mutable(self):
        changes_in = [Change(5, pn) for pn in ['3', '1', '5']]
        rb = RowBlock(changes_in)

        # Make a local reference to rb.changes, and modify it...
        changes_out = rb.changes
        changes_out.pop()

        # ... then make sure the original hasn't changed
        self.assertEqual(len(changes_in), 3)
        self.assertEqual(len(rb.changes), 3)
        self.assertEqual(rb.changes, changes_in)

    def test_row_block_subscript_bounds(self):
        rb = RowBlock([Change(5, pn) for pn in ['3', '1', '5']])

        self.assertRaises(IndexError, lambda: rb[-1])
        self.assertEqual(rb[0], '12345')
        self.assertEqual(rb[3], '32415')
        self.assertRaises(IndexError, lambda: rb[4])

        self.assertRaises(IndexError, lambda: rb.__setitem__(-1, Row(5)))
        rb[0] = Row(5)  # Should succeed
        rb[3] = Row(5)
        self.assertRaises(IndexError, lambda: rb.__setitem__(4, Row(5)))

    def test_row_block_recalculate_bounds(self):
        rb = RowBlock([Change(5, pn) for pn in ['3', '1', '5']])

        self.assertRaises(IndexError, lambda: rb.recalculate(-1))
        rb.recalculate(0)
        rb.recalculate(3)
        self.assertRaises(IndexError, lambda: rb.recalculate(4))

    def test_row_block_iterator(self):
        rb = RowBlock([Change(5, pn) for pn in ['3', '1', '5']])

        self.assertEqual(list(rb), ['12345', '21354', '23145', '32415'])
