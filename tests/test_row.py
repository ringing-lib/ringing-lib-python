import itertools
import unittest

from ringing import Row


class RowTest(unittest.TestCase):
    def test_row_constructor_exceptions(self):
        self.assertRaises(ValueError, lambda: Row(-1))
        self.assertRaises(ValueError, lambda: Row(257))
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
        self.assertRaises(ValueError, lambda: r.find(257))

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

    def test_row_inverse_tilde(self):
        self.assertEqual(~Row('654321'), '654321')
        self.assertEqual(~Row('312'), '231')
        self.assertEqual(~Row('18234567'), '13456782')

    def test_row_subscript_bounds(self):
        r = Row(6)
        self.assertRaises(IndexError, lambda: r[-1])
        self.assertEqual(r[0], 0)
        self.assertEqual(r[5], 5)
        self.assertRaises(IndexError, lambda: r[6])
