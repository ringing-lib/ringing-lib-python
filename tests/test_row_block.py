import unittest

from ringing import Row, Change, RowBlock


class RowBlockTest(unittest.TestCase):
    def test_row_block_constructor_exceptions(self):
        self.assertRaises(TypeError, lambda: RowBlock(self))
        self.assertRaises(TypeError, lambda: RowBlock([self]))
        self.assertRaises(TypeError, lambda: RowBlock([], self))
