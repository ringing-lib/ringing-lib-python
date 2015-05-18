import unittest

from ringing import RowBlock, Change


class RowBlockTest(unittest.TestCase):
    def test_row_block_constructors(self):
        changes = []
        changes.append(Change(5, '3'))
        changes.append(Change(5, '1'))
        changes.append(Change(5, '5'))

        rb = RowBlock(changes)
        self.assertEqual(rb.size, 4)
        self.assertEqual(rb[0], '12345')
        self.assertEqual(rb[1], '21354')
        self.assertEqual(rb[2], '23145')
        self.assertEqual(rb[3], '32415')

        rb = RowBlock(changes, '54321')
        self.assertEqual(rb[2], '43521')

    def test_row_block_set_start(self):
        changes = []
        changes.append(Change(5, '3'))
        changes.append(Change(5, '1'))
        changes.append(Change(5, '5'))

        rb = RowBlock(changes)
        rb.set_start('54321')
        rb.recalculate()

        self.assertEqual(rb[2], '43521')

    def test_row_block_recalculate(self):
        changes = []
        changes.append(Change(5, '3'))
        changes.append(Change(5, '1'))
        changes.append(Change(5, '5'))

        rb = RowBlock(changes)
        rb[2] = '54321'
        rb.recalculate(2)

        self.assertEqual(rb.size, 4)
        self.assertEqual(rb[0], '12345')
        self.assertEqual(rb[1], '21354')
        self.assertEqual(rb[2], '54321')
        self.assertEqual(rb[3], '45231')

    def test_row_block_get_changes(self):
        changes = []
        rb = RowBlock(changes)

        self.assertEqual(rb.changes, changes)
