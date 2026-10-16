import pytest

from ringing import Bell, Change, Method
from tests import MAX_BELL_NUMBER


class TestMethod:
    def test_method_constructor_exceptions(self):
        with pytest.raises(TypeError):
            Method(input=self)

        with pytest.raises(ValueError):
            Method(bells=-1)
        Method(bells=0)
        Method(bells=MAX_BELL_NUMBER)
        with pytest.raises(ValueError):
            Method(bells=MAX_BELL_NUMBER + 1)

        with pytest.raises(TypeError):
            Method(name=self)

        # https://github.com/ringing-lib/ringing-lib-python/issues/6
        with pytest.raises(ValueError):
            Method('3')

    def test_method_is_symmetric_limits(self):
        m = Method('&-1-1-1,2', 6)
        with pytest.raises(ValueError):
            m.is_symmetric(-1)
        m.is_symmetric(0)
        m.is_symmetric(5)
        with pytest.raises(IndexError):
            m.is_symmetric(6)

    def test_method_is_palindromic_limits(self):
        m = Method('&-1-1-1,2', 6)
        with pytest.raises(ValueError):
            m.is_palindromic(-1)
        m.is_palindromic(0)
        m.is_palindromic(5)
        with pytest.raises(IndexError):
            m.is_palindromic(6)

    def test_method_is_plain_limits(self):
        m = Method('&-1-1-1,2', 6)
        with pytest.raises(ValueError):
            m.is_plain(-1)
        m.is_plain(0)
        m.is_plain(5)
        with pytest.raises(IndexError):
            m.is_plain(6)

    def test_method_has_dodges_limits(self):
        m = Method('&-1-1-1,2', 6)
        with pytest.raises(ValueError):
            m.has_dodges(-1)
        m.has_dodges(0)
        m.has_dodges(5)
        with pytest.raises(IndexError):
            m.has_dodges(6)

    def test_method_has_places_limits(self):
        m = Method('&-1-1-1,2', 6)
        with pytest.raises(ValueError):
            m.has_places(-1)
        m.has_places(0)
        m.has_places(5)
        with pytest.raises(IndexError):
            m.has_places(6)

    def test_method_symmetry_point_limits(self):
        m = Method('&-1-1-1,2', 6)
        with pytest.raises(ValueError):
            m.symmetry_point(-1)
        m.symmetry_point(0)
        m.symmetry_point(5)
        with pytest.raises(IndexError):
            m.symmetry_point(6)

    def test_method_takes_bell_types(self):
        m = Method('&-1-1-1,2', 6)

        m.is_symmetric(Bell(0))
        m.is_symmetric('1')
        m.is_symmetric(0)

        m.is_palindromic(Bell(0))
        m.is_palindromic('1')
        m.is_palindromic(0)

        m.is_plain(Bell(0))
        m.is_plain('1')
        m.is_plain(0)

        m.has_dodges(Bell(0))
        m.has_dodges('1')
        m.has_dodges(0)

        m.has_places(Bell(0))
        m.has_places('1')
        m.has_places(0)

        m.symmetry_point(Bell(0))
        m.symmetry_point('1')
        m.symmetry_point(0)

    def test_method_symmetry_point_assertion(self):
        # Executing the following causes assertion failures in the library.
        # Work around by raising ValueError instead.
        with pytest.raises(ValueError):
            Method(3, 6).is_palindromic()
        with pytest.raises(ValueError):
            Method(3, 6).is_palindromic(0)
        with pytest.raises(ValueError):
            Method(3, 6).symmetry_point()
        with pytest.raises(ValueError):
            Method(3, 6).symmetry_point(0)
        with pytest.raises(ValueError):
            Method(3, 6).format(symmetry=True)
        with pytest.raises(ValueError):
            Method(3, 6).format(full_symmetry=True)

        # is_symmetric() shouldn't exhibit this problem
        assert not Method(3, 6).is_symmetric()
        assert not Method(3, 6).is_symmetric(0)

        # Make sure __repr__ handles method with odd numbers of changes
        assert repr(Method(2, 4)) == "Method('1234.1234', 4, 'Untitled')"
        assert repr(Method(3, 4)) == "Method('+1234.1234.1234', 4, 'Untitled')"

    def test_method_index_limits(self):
        m = Method('&-1-1-1,2', 6)

        with pytest.raises(IndexError):
            m[-1]
        m[0]
        m[m.size - 1]
        with pytest.raises(IndexError):
            m[m.size]

        def assign_change(index):
            m[index] = Change(6)

        with pytest.raises(IndexError):
            assign_change(-1)
        assign_change(0)
        assign_change(m.size - 1)
        with pytest.raises(IndexError):
            assign_change(m.size)
