import sys
import unittest

from ringing import Bell


class BellTest(unittest.TestCase):
    def test_bell_bytes_bytes(self):
        self.assertIsInstance(bytes(Bell(5)), bytes)

    def test_bell_unicode_unicode(self):
        if sys.version_info.major < 3:
            self.assertIsInstance(unicode(Bell(5)), unicode)
        else:
            self.assertIsInstance(Bell(5).__unicode__(), str)

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
