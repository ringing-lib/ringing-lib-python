import sys
import unittest

from ringing import Bell
from tests import MAX_BELL_NUMBER


class BellTest(unittest.TestCase):
    def test_bell_constructor(self):
        self.assertEqual(Bell(Bell(10)), 10)
        self.assertEqual(Bell('e'), 10)
        self.assertEqual(Bell(u'e'), 10)
        self.assertEqual(Bell(b'e'), 10)
        self.assertEqual(Bell('E'), 10)
        self.assertEqual(Bell(u'E'), 10)
        self.assertEqual(Bell(b'E'), 10)

    def test_bell_constructor_exceptions(self):
        self.assertRaises(TypeError, lambda: Bell(self))

        self.assertRaises(ValueError(-1))
        Bell(0)
        Bell(MAX_BELL_NUMBER)
        self.assertRaises(ValueError, lambda: Bell(MAX_BELL_NUMBER + 1))

        self.assertRaises(ValueError, lambda: Bell('%'))
        self.assertRaises(ValueError, lambda: Bell(u'%'))
        self.assertRaises(ValueError, lambda: Bell(b'%'))

    def test_bell_bytes_bytes(self):
        self.assertIs(type(bytes(Bell(5))), bytes)

    def test_bell_unicode_unicode(self):
        if sys.version_info[0] < 3:
            self.assertIs(type(unicode(Bell(5))), unicode)
        else:
            self.assertIs(type(Bell(5).__unicode__()), str)

    def test_is_symbol(self):
        self.assertTrue(Bell.is_symbol('1'))
        self.assertTrue(Bell.is_symbol(u'1'))
        self.assertTrue(Bell.is_symbol(b'1'))
        self.assertTrue(Bell.is_symbol('a'))
        self.assertTrue(Bell.is_symbol(u'a'))
        self.assertTrue(Bell.is_symbol(b'a'))
        self.assertTrue(Bell.is_symbol('A'))
        self.assertTrue(Bell.is_symbol(u'A'))
        self.assertTrue(Bell.is_symbol(b'A'))

        self.assertFalse(Bell.is_symbol('%'))
        self.assertFalse(Bell.is_symbol(u'%'))
        self.assertFalse(Bell.is_symbol(b'%'))
