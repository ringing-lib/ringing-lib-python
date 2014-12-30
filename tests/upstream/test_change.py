import unittest

from ringing import Change


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

    def test_change_reverse(self):
        self.assertEqual(Change(5, '1').reverse(), Change(5, '5'))
        self.assertEqual(Change(6, '16').reverse(), Change(6, '16'))
        self.assertEqual(Change(8, 'X').reverse(), Change(8, 'X'))
        self.assertEqual(Change(4, '12').reverse(), Change(4, '34'))

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

    def test_change_sign(self):
        self.assertEqual(Change().sign(), +1)
        self.assertEqual(Change(4).sign(), +1)
        self.assertEqual(Change(9).sign(), +1)
        self.assertEqual(Change(9, '1').sign(), +1)
        self.assertEqual(Change(9, '9').sign(), +1)
        self.assertEqual(Change(9, '129').sign(), -1)
        self.assertEqual(Change(6, '12').sign(), +1)
        self.assertEqual(Change(6, '-').sign(), -1)
        self.assertEqual(Change(8, '-').sign(), +1)

    def test_change_internal(self):
        self.assertFalse(Change().internal())
        self.assertFalse(Change(1).internal())
        self.assertFalse(Change(2).internal())
        self.assertTrue(Change(3).internal())
        self.assertFalse(Change(5, '1').internal())
        self.assertTrue(Change(5, '125').internal())
        self.assertFalse(Change(6, '-').internal())
        self.assertFalse(Change(6, '16').internal())
        self.assertTrue(Change(6, '1256').internal())
        self.assertTrue(Change(4, '1234').internal())
        self.assertTrue(Change(8, '4').internal())
        self.assertTrue(Change(8, '3').internal())
        self.assertFalse(Change(8, '1').internal())

    def test_change_count_places(self):
        self.assertEqual(Change(8).count_places(), 8)
        self.assertEqual(Change(8, '3').count_places(), 2)
        self.assertEqual(Change(8, '6').count_places(), 2)
        self.assertEqual(Change(8, '36').count_places(), 2)
        self.assertEqual(Change(8, '18').count_places(), 2)
        self.assertEqual(Change(8, '78').count_places(), 2)
        self.assertEqual(Change(9, '7').count_places(), 1)
        self.assertEqual(Change(9, '1').count_places(), 1)
        self.assertEqual(Change(9, '9').count_places(), 1)

    def test_change_comparison(self):
        self.assertTrue(Change(6, '1234') < Change(8, '56'))
        self.assertTrue(Change(6, '1234') <= Change(8, '56'))
        self.assertFalse(Change(6, '1234') > Change(8, '56'))
        self.assertFalse(Change(6, '1234') >= Change(8, '56'))

        self.assertTrue(Change(6, '1234') > Change(6, '56'))
        self.assertTrue(Change(6, '1234') >= Change(6, '56'))
        self.assertFalse(Change(6, '1234') < Change(6, '56'))
        self.assertFalse(Change(6, '1234') <= Change(6, '56'))

        self.assertFalse(Change(6, 'X') > Change(6, 'X'))
        self.assertTrue(Change(6, 'X') >= Change(6, 'X'))
        self.assertFalse(Change(6, 'X') < Change(6, 'X'))
        self.assertTrue(Change(6, 'X') <= Change(6, 'X'))

        self.assertTrue(Change(6) < Change(6, '3456'))
        self.assertTrue(Change(6, '3456') < Change(6, '56'))
        self.assertTrue(Change(6, '56') < Change(6, '36'))
        self.assertTrue(Change(6, '36') < Change(6, '16'))

    def test_change_output(self):
        string = '.'.join(map(str, [
            Change(6, '-'),
            Change(6, '3'),
            Change(6, '-'),
            Change(6, '4'),
        ]))
        self.assertEqual(string, 'X.36.X.14')
