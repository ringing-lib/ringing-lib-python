import itertools
import unittest

from ringing import Bell, Row
from tests import MAX_BELL_NUMBER


class RowTest(unittest.TestCase):
    def test_row_constructor_exceptions(self):
        self.assertRaises(ValueError, lambda: Row(-1))
        Row(0)
        Row(MAX_BELL_NUMBER)
        self.assertRaises(ValueError, lambda: Row(MAX_BELL_NUMBER + 1))
        self.assertRaises(TypeError, lambda: Row(self))

    def test_row_equals_string_types(self):
        self.assertEqual(Row('123456'), '123456')

        self.assertEqual(Row(b'123456'), b'123456')
        self.assertEqual(Row(u'123456'), u'123456')

        self.assertEqual(bytes(Row('123456')), b'123456')

        try:
            self.assertEqual(unicode(Row('123456')), u'123456')
        except NameError:
            pass

    def test_row_find(self):
        r = Row('615423')

        self.assertEqual(r.find(0), 1)
        self.assertEqual(r.find(1), 4)
        self.assertEqual(r.find(2), 5)
        self.assertEqual(r.find(3), 3)
        self.assertEqual(r.find(4), 2)
        self.assertEqual(r.find(5), 0)
        self.assertEqual(r.find(6), 6)

        self.assertRaises(ValueError, lambda: r.find(-1))
        r.find(0)
        r.find(MAX_BELL_NUMBER)
        self.assertRaises(ValueError, lambda: r.find(MAX_BELL_NUMBER + 1))
        self.assertRaises(TypeError, lambda: r.find(self))

        self.assertEqual(r.find(Bell(0)), 1)
        self.assertEqual(r.find(Bell('1')), 1)

    def test_row_conjugator(self):
        x = Row('2143')
        y = Row('3412')

        r = Row.conjugator(x, y)
        self.assertEqual(y, ~r * x * r)

        self.assertFalse(Row.conjugator(x, 4))

    def test_row_are_conjugate(self):
        conj_class = list(map(Row, ['2143', '3412', '4321']))

        for r1, r2 in itertools.product(conj_class, conj_class):
            self.assertTrue(Row.are_conjugate(r1, r2))

        for r in conj_class:
            self.assertFalse(Row.are_conjugate(r, 4))

    def test_operators_return_not_implemented(self):
        # Arithmetic operator returns NotImplemented when given unknown types
        self.assertEqual(Row().__lt__(self), NotImplemented)
        self.assertEqual(Row().__le__(self), NotImplemented)
        self.assertEqual(Row().__eq__(self), NotImplemented)
        self.assertEqual(Row().__ne__(self), NotImplemented)
        self.assertEqual(Row().__gt__(self), NotImplemented)
        self.assertEqual(Row().__ge__(self), NotImplemented)
        self.assertEqual(Row().__mul__(self), NotImplemented)
        self.assertEqual(Row().__rmul__(self), NotImplemented)
        self.assertEqual(Row().__truediv__(self), NotImplemented)
        self.assertEqual(Row().__rtruediv__(self), NotImplemented)

        # ... but passes through errors parsing known types.
        self.assertRaises(ValueError, lambda: Row().__lt__('!'))
        self.assertRaises(ValueError, lambda: Row().__le__('!'))
        self.assertRaises(ValueError, lambda: Row().__eq__('!'))
        self.assertRaises(ValueError, lambda: Row().__ne__('!'))
        self.assertRaises(ValueError, lambda: Row().__gt__('!'))
        self.assertRaises(ValueError, lambda: Row().__ge__('!'))
        self.assertRaises(ValueError, lambda: Row().__mul__('!'))
        self.assertRaises(ValueError, lambda: Row().__rmul__('!'))
        self.assertRaises(ValueError, lambda: Row().__truediv__('!'))
        self.assertRaises(ValueError, lambda: Row().__rtruediv__('!'))

        try:
            self.assertEqual(Row().__div__(self), NotImplemented)
            self.assertRaises(ValueError, lambda: Row().__div__('!'))
        except AttributeError:
            pass  # Ignore (Python 3 doesn't create __div__)

    def test_row_repr(self):
        self.assertEqual(repr(Row()), 'Row()')
        self.assertEqual(repr(Row('123456')), "Row('123456')")

    def test_row_inverse_tilde(self):
        self.assertEqual(~Row('654321'), '654321')
        self.assertEqual(~Row('312'), '231')
        self.assertEqual(~Row('18234567'), '13456782')

    def test_row_subscript_returns_bell(self):
        r = Row(6)
        self.assertEqual(type(r[0]), Bell)

    def test_row_subscript_bounds(self):
        r = Row(6)
        self.assertRaises(IndexError, lambda: r[-1])
        self.assertEqual(r[0], 0)
        self.assertEqual(r[5], 5)
        self.assertRaises(IndexError, lambda: r[6])
