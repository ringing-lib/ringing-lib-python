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
