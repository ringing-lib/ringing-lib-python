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

    def test_row_subscript_bounds(self):
        r = Row(6)
        self.assertRaises(IndexError, lambda: r[-1])
        self.assertRaises(IndexError, lambda: r[6])

    def test_row_inverse_tilde(self):
        self.assertEqual(~Row('654321'), '654321')
        self.assertEqual(~Row('312'), '231')
        self.assertEqual(~Row('18234567'), '13456782')

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
