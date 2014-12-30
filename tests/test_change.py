import unittest

from ringing import Change


class ChangeTest(unittest.TestCase):
    def test_change_constructor_exceptions(self):
        self.assertRaises(ValueError, lambda: Change(-1))
        self.assertRaises(ValueError, lambda: Change(257))
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
