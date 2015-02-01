import unittest

from ringing import Change, Method
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

    def test_method_is_symmetric_limits(self):
        m = Method('&-1-1-1,2', 6)
        self.assertRaises(IndexError, lambda: m.is_symmetric(-1))
        m.is_symmetric(0)
        m.is_symmetric(5)
        self.assertRaises(IndexError, lambda: m.is_symmetric(6))

    def test_method_is_palindromic_limits(self):
        m = Method('&-1-1-1,2', 6)
        self.assertRaises(IndexError, lambda: m.is_palindromic(-1))
        m.is_palindromic(0)
        m.is_palindromic(5)
        self.assertRaises(IndexError, lambda: m.is_palindromic(6))

    def test_method_is_plain_limits(self):
        m = Method('&-1-1-1,2', 6)
        self.assertRaises(IndexError, lambda: m.is_plain(-1))
        m.is_plain(0)
        m.is_plain(5)
        self.assertRaises(IndexError, lambda: m.is_plain(6))

    def test_method_has_dodges_limits(self):
        m = Method('&-1-1-1,2', 6)
        self.assertRaises(IndexError, lambda: m.has_dodges(-1))
        m.has_dodges(0)
        m.has_dodges(5)
        self.assertRaises(IndexError, lambda: m.has_dodges(6))

    def test_method_has_places_limits(self):
        m = Method('&-1-1-1,2', 6)
        self.assertRaises(IndexError, lambda: m.has_places(-1))
        m.has_places(0)
        m.has_places(5)
        self.assertRaises(IndexError, lambda: m.has_places(6))

    def test_method_symmetry_point_limits(self):
        m = Method('&-1-1-1,2', 6)
        self.assertRaises(IndexError, lambda: m.symmetry_point(-1))
        m.symmetry_point(0)
        m.symmetry_point(5)
        self.assertRaises(IndexError, lambda: m.symmetry_point(6))

    def test_method_symmetry_point_assertion(self):
        # Executing the following causes assertion failures in the library.
        # Work around by raising ValueError instead.
        self.assertRaises(ValueError, lambda: Method(3, 6).is_palindromic())
        self.assertRaises(ValueError, lambda: Method(3, 6).is_palindromic(0))
        self.assertRaises(ValueError, lambda: Method(3, 6).symmetry_point())
        self.assertRaises(ValueError, lambda: Method(3, 6).symmetry_point(0))
        self.assertRaises(ValueError,
                          lambda: Method(3, 6).format(symmetry=True))
        self.assertRaises(ValueError,
                          lambda: Method(3, 6).format(full_symmetry=True))

        # is_symmetric() shouldn't exhibit this problem
        self.assertFalse(Method(3, 6).is_symmetric())
        self.assertFalse(Method(3, 6).is_symmetric(0))

        # Make sure __repr__ handles method with odd numbers of changes
        self.assertEqual(
            repr(Method(2, 4)),
            "Method('1234.1234', 4, 'Untitled')"
        )
        self.assertEqual(
            repr(Method(3, 4)),
            "Method('+1234.1234.1234', 4, 'Untitled')"
        )

    def test_method_index_limits(self):
        m = Method('&-1-1-1,2', 6)

        self.assertRaises(IndexError, lambda: m[-1])
        m[0]
        m[m.size - 1]
        self.assertRaises(IndexError, lambda: m[m.size])

        def assign_change(index):
            m[index] = Change(6)

        self.assertRaises(IndexError, lambda: assign_change(-1))
        assign_change(0)
        assign_change(m.size - 1)
        self.assertRaises(IndexError, lambda: assign_change(m.size))
