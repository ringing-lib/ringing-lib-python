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
