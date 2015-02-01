import unittest

from ringing import Method
from tests import MAX_BELL_NUMBER

class MethodTest(unittest.TestCase):
    def test_method_constructor_exceptions(self):
        self.assertRaises(TypeError, lambda: Method(input=self))

        self.assertRaises(ValueError, lambda: Method(bells=-1))
        Method(bells=0)
        Method(bells=MAX_BELL_NUMBER)
        self.assertRaises(
            ValueError,
            lambda: Method(bells=MAX_BELL_NUMBER + 1)
        )

        self.assertRaises(TypeError, lambda: Method(name=self))
