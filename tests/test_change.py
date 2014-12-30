import unittest

from change import Change


class ChangeTest(unittest.TestCase):
    def test_change_constructor_exceptions(self):
        self.assertRaises(ValueError, lambda: Change(-1))
        self.assertRaises(ValueError, lambda: Change(257))
        self.assertRaises(TypeError, lambda: Change(self))
        self.assertRaises(TypeError, lambda: Change(1, self))
