import unittest

from ringing import Row, Change, RowBlock


class RowBlockTest(unittest.TestCase):
    def test_row_block_constructor_exceptions(self):
        self.assertRaises(TypeError, lambda: RowBlock(self))
        self.assertRaises(TypeError, lambda: RowBlock([self]))
        self.assertRaises(TypeError, lambda: RowBlock([], self))

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
