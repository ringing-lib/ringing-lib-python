import unittest

from ringing import Bell, Change
from tests import MAX_BELL_NUMBER


class ChangeTest(unittest.TestCase):
    def test_change_constructor_exceptions(self):
        self.assertRaises(ValueError, lambda: Change(-1))
        Change(0)
        Change(MAX_BELL_NUMBER)
        self.assertRaises(ValueError, lambda: Change(MAX_BELL_NUMBER + 1))

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
        c.set(MAX_BELL_NUMBER, 'X')
        self.assertRaises(ValueError, lambda: c.set(MAX_BELL_NUMBER + 1, 'X'))

        self.assertRaises(TypeError, lambda: c.set(self, 'X'))
        self.assertRaises(TypeError, lambda: c.set(1, self))

        self.assertRaises(ValueError, lambda: Change(5, 'XYZ'))

    def test_change_set_returns_none(self):
        c = Change()
        self.assertEqual(c.set(4, 'X'), None)

    def test_index_method_bounds(self):
        c = Change(6)

        self.assertRaises(ValueError, lambda: c.find_swap(-1))
        self.assertFalse(c.find_swap(0))
        self.assertFalse(c.find_swap(4))
        self.assertRaises(IndexError, lambda: c.find_swap(5))

        self.assertRaises(ValueError, lambda: c.find_place(-1))
        self.assertTrue(c.find_place(0))
        self.assertTrue(c.find_place(5))
        self.assertRaises(IndexError, lambda: c.find_place(6))

        self.assertRaises(ValueError, lambda: c.swap_pair(-1))
        self.assertTrue(c.swap_pair(0))
        self.assertTrue(c.swap_pair(4))
        self.assertRaises(IndexError, lambda: c.swap_pair(5))

    def test_index_method_types(self):
        c = Change(6)

        c.find_swap(Bell(0))
        c.find_swap('1')
        c.find_swap(0)

        c.find_place(Bell(0))
        c.find_place('1')
        c.find_place(0)

        c.swap_pair(Bell(0))
        c.swap_pair('1')
        c.swap_pair(0)

        self.assertRaises(TypeError, lambda: c.find_swap(self))
        self.assertRaises(TypeError, lambda: c.find_place(self))
        self.assertRaises(TypeError, lambda: c.swap_pair(self))

    def test_operators_return_not_implemented(self):
        # Arithmetic operator returns NotImplemented when given unknown types
        self.assertEqual(Change().__lt__(self), NotImplemented)
        self.assertEqual(Change().__le__(self), NotImplemented)
        self.assertEqual(Change().__eq__(self), NotImplemented)
        self.assertEqual(Change().__ne__(self), NotImplemented)
        self.assertEqual(Change().__gt__(self), NotImplemented)
        self.assertEqual(Change().__ge__(self), NotImplemented)
        self.assertEqual(Change().__mul__(self), NotImplemented)
        self.assertEqual(Change().__rmul__(self), NotImplemented)

        # ... but passes through errors parsing known types.
        self.assertRaises(ValueError, lambda: Change().__lt__('!'))
        self.assertRaises(ValueError, lambda: Change().__le__('!'))
        self.assertRaises(ValueError, lambda: Change().__eq__('!'))
        self.assertRaises(ValueError, lambda: Change().__ne__('!'))
        self.assertRaises(ValueError, lambda: Change().__gt__('!'))
        self.assertRaises(ValueError, lambda: Change().__ge__('!'))

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
        c * 0
        c * MAX_BELL_NUMBER
        self.assertRaises(ValueError, lambda: c * (MAX_BELL_NUMBER + 1))

        self.assertRaises(ValueError, lambda:-1 * c)
        0 * c
        MAX_BELL_NUMBER * c
        self.assertRaises(ValueError, lambda: (MAX_BELL_NUMBER + 1) * c)

    def test_bell_multiply_types(self):
        c = Change(6, '14')

        c * Bell(0)
        c * '1'
        c * 0

        Bell(0) * c
        '1' * c
        0 * c

        self.assertRaises(TypeError, lambda: c * self)
        self.assertRaises(TypeError, lambda: self * c)
