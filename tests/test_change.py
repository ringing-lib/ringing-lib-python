import unittest

from ringing import Change


class ChangeTest(unittest.TestCase):
    def test_change_constructor_exceptions(self):
        self.assertRaises(ValueError, lambda: Change(-1))
        self.assertRaises(ValueError, lambda: Change(256))
        self.assertRaises(TypeError, lambda: Change(self))
        self.assertRaises(TypeError, lambda: Change(1, self))

    def test_change_equals_string_types(self):
        self.assertEqual(Change(6, '16'), '16')

        self.assertEqual(Change(6, b'16'), b'16')
        self.assertEqual(Change(6, u'16'), u'16')

        self.assertEqual(bytes(Change(6, '16')), b'16')

        try:
            self.assertEqual(unicode(Change(6, '16')), u'16')
        except NameError:
            pass

    def test_change_set_exceptions(self):
        c = Change()

        self.assertRaises(ValueError, lambda: c.set(-1, 'X'))
        c.set(0, 'X')
        c.set(255, 'X')
        self.assertRaises(ValueError, lambda: c.set(256, 'X'))

        self.assertRaises(TypeError, lambda: c.set(self, 'X'))
        self.assertRaises(TypeError, lambda: c.set(1, self))

        self.assertRaises(ValueError, lambda: Change(5, 'XYZ'))

    def test_change_set_returns_none(self):
        c = Change()
        self.assertEqual(c.set(4, 'X'), None)

    def test_index_method_bounds(self):
        c = Change(6)

        self.assertRaises(IndexError, lambda: c.find_swap(-1))
        self.assertFalse(c.find_swap(0))
        self.assertFalse(c.find_swap(4))
        self.assertRaises(IndexError, lambda: c.find_swap(5))

        self.assertRaises(IndexError, lambda: c.find_place(-1))
        self.assertTrue(c.find_place(0))
        self.assertTrue(c.find_place(5))
        self.assertRaises(IndexError, lambda: c.find_place(6))

        self.assertRaises(IndexError, lambda: c.swap_pair(-1))
        self.assertTrue(c.swap_pair(0))
        self.assertTrue(c.swap_pair(4))
        self.assertRaises(IndexError, lambda: c.swap_pair(5))

    def test_change_repr(self):
        self.assertEqual(repr(Change()), 'Change()')
        self.assertEqual(repr(Change(4)), "Change(4, '1234')")
        self.assertEqual(repr(Change(4, 'X')), "Change(4, 'X')")

    def test_bell_multiply_order(self):
        c = Change(6, '14')

        self.assertEqual(0 * c, 0)
        self.assertEqual(1 * c, 2)
        self.assertEqual(2 * c, 1)
        self.assertEqual(3 * c, 3)
        self.assertEqual(4 * c, 5)

        self.assertEqual(c * 0, 0)
        self.assertEqual(c * 1, 2)
        self.assertEqual(c * 2, 1)
        self.assertEqual(c * 3, 3)
        self.assertEqual(c * 4, 5)

    def test_bell_multiply_bounds(self):
        c = Change(6, '14')

        self.assertRaises(ValueError, lambda: c * -1)
        self.assertRaises(ValueError, lambda: c * 256)
