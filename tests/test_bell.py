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

        self.assertRaises(ValueError, lambda: Bell(-1))
        Bell(0)
        Bell(MAX_BELL_NUMBER)
        self.assertRaises(ValueError, lambda: Bell(MAX_BELL_NUMBER + 1))

        self.assertRaises(ValueError, lambda: Bell('%'))
        self.assertRaises(ValueError, lambda: Bell(u'%'))
        self.assertRaises(ValueError, lambda: Bell(b'%'))

    def test_bell_bytes_bytes(self):
        self.assertEqual(type(bytes(Bell(5))), bytes)

    def test_bell_unicode_unicode(self):
        if sys.version_info[0] < 3:
            self.assertEqual(type(unicode(Bell(5))), unicode)
        else:
            self.assertEqual(type(Bell(5).__unicode__()), str)

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


class BellSymbolsTest(unittest.TestCase):
    NEW_SYMBOLS = 'abcdef%'

    def setUp(self):
        Bell.set_symbols(self.NEW_SYMBOLS)

    def tearDown(self):
        Bell.set_symbols()

    def test_symbols_set(self):
        for index, character in enumerate(self.NEW_SYMBOLS):
            self.assertEqual(Bell(index), character)

    def test_is_symbol(self):
        for character in self.NEW_SYMBOLS:
            self.assertTrue(Bell.is_symbol(character))

    def test_max_bells(self):
        self.assertEqual(Bell.MAX_BELLS, len(self.NEW_SYMBOLS))

    def test_symbols_restored(self):
        Bell.set_symbols()
        self.assertEqual(Bell(0).to_char(), '1')
