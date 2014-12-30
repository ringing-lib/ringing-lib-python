import unittest

from change import Change


class ChangeTest(unittest.TestCase):
    def test_change_invalid(self):
        self.assertRaises(ValueError, lambda: Change(5, '18'))
        self.assertRaises(ValueError, lambda: Change(5, 'XYZ'))
        self.assertRaises(ValueError, lambda: Change(5, '!$'))
        self.assertRaises(ValueError, lambda: Change(5, ''))
        self.assertRaises(ValueError, lambda: Change(5, '321'))
        self.assertRaises(ValueError, lambda: Change(5, '11'))
        self.assertRaises(ValueError, lambda: Change(5, '12 3'))

    def test_change_print(self):
        self.assertEqual(str(Change()), '')
        self.assertEqual(str(Change(8, '-')), 'X')
        self.assertEqual(str(Change(8, '18')), '18')
        self.assertEqual(str(Change(10, '18')), '18')
        self.assertEqual(str(Change(10, '4')), '14')
        self.assertEqual(str(Change(10, '129')), '1290')
        self.assertEqual(str(Change(16, 'E')), 'ED')
