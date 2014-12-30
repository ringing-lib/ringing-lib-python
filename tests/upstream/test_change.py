import unittest

from change import Change


class ChangeTest(unittest.TestCase):
    def test_change_equals(self):
        self.assertTrue(Change() == Change(0, ''))
        self.assertTrue(Change(3) == Change(3, '123'))
        self.assertTrue(Change(4) == Change(4, '1234'))
        self.assertTrue(Change(5, '3') == Change(5, '3'))
        self.assertTrue(Change(6, '1') != Change(6, '5'))
        self.assertTrue(Change(8, 'X') == Change(8, '-'))
        self.assertTrue(Change(6, '-') != Change(8, '-'))
        self.assertTrue(Change(6, '-') != Change(8, '78'))

    def test_change_copy(self):
        a = Change(6, '12')
        c = Change(a)
        self.assertEqual(a, c)

        # Tests involving change::swap() omitted.

    def test_change_invalid(self):
        self.assertRaises(ValueError, lambda: Change(5, '18'))
        self.assertRaises(ValueError, lambda: Change(5, 'XYZ'))
        self.assertRaises(ValueError, lambda: Change(5, '!$'))
        self.assertRaises(ValueError, lambda: Change(5, ''))
        self.assertRaises(ValueError, lambda: Change(5, '321'))
        self.assertRaises(ValueError, lambda: Change(5, '11'))
        self.assertRaises(ValueError, lambda: Change(5, '12 3'))

    def test_change_implicit_places(self):
        self.assertEqual(Change(6, '4'), Change(6, '14'))
        self.assertEqual(Change(5, '-'), Change(5, '5'))
        self.assertEqual(Change(7, '12'), Change(7, '127'))

        self.assertRaises(ValueError, lambda: Change(5, '15'))

    def test_change_print(self):
        self.assertEqual(str(Change()), '')
        self.assertEqual(str(Change(8, '-')), 'X')
        self.assertEqual(str(Change(8, '18')), '18')
        self.assertEqual(str(Change(10, '18')), '18')
        self.assertEqual(str(Change(10, '4')), '14')
        self.assertEqual(str(Change(10, '129')), '1290')
        self.assertEqual(str(Change(16, 'E')), 'ED')

    def test_change_bells(self):
        self.assertEqual(Change().bells, 0)
        self.assertEqual(Change(7).bells, 7)
        self.assertEqual(Change(8, '14').bells, 8)

    def test_change_output(self):
        string = '.'.join(map(str, [
            Change(6, '-'),
            Change(6, '3'),
            Change(6, '-'),
            Change(6, '4'),
        ]))
        self.assertEqual(string, 'X.36.X.14')
