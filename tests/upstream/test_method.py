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

    def test_method_lh(self):
        self.assertEqual(Method().lead_head(), '')
        self.assertEqual(Method('&-1-1-1-1,2', 8).lead_head(), '13527486')
        self.assertEqual(Method('&-1-1-1-1,1', 8).lead_head(), '12345678')
        self.assertEqual(Method('&-3-4-2-3-4-5,2', 6).lead_head(), '156342')
        self.assertEqual(Method('+5.3.1.3.1.3', 5).lead_head(), '24153')

    def test_method_issym(self):
        self.assertTrue(Method().is_symmetric())
        self.assertTrue(Method('&-1-1-1,2', 6).is_symmetric())
        self.assertTrue(Method('&-1-1-1,1', 6).is_symmetric())
        self.assertFalse(Method('3,&1-1-1-', 6).is_symmetric())
        self.assertFalse(Method('3.1.5.1.5.1.5.1.5.123', 5).is_symmetric())
        self.assertTrue(Method('&-4-36-5-1,8', 8).is_symmetric())
        self.assertFalse(Method('+5.3.1.3.1.3', 5).is_symmetric())
