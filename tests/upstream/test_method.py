import unittest

from ringing import Method


class MethodTest(unittest.TestCase):
    def test_method_length(self):
        self.assertEqual(Method('&-12,16', 6).length, 4)
        self.assertEqual(Method('&-12,16', 6).size, 4)
        self.assertEqual(Method().size, 0)

    def test_method_bells(self):
        self.assertEqual(Method('', 6).bells, 6)
        self.assertEqual(Method('&-1-1-1,2', 6).bells, 6)
