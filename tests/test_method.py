import pytest

from ringing import Bell, Change, Method
from tests import MAX_BELL_NUMBER



def test_constructor_exceptions() -> None:
    with pytest.raises(TypeError):
        Method(input=[])

    with pytest.raises(ValueError):
        Method(bells=-1)
    Method(bells=0)
    Method(bells=MAX_BELL_NUMBER)
    with pytest.raises(ValueError):
        Method(bells=MAX_BELL_NUMBER + 1)

    with pytest.raises(TypeError):
        Method(name=[])

    # https://github.com/ringing-lib/ringing-lib-python/issues/6
    with pytest.raises(ValueError):
        Method('3')


def test_unicode_name() -> None:
    m = Method('&-1-1-1,2', 6, name='•')
    assert m.name == '•'
    assert m.full_name() == '• Bob Minor'
    assert str(m) == '• Bob Minor'


def test_is_symmetric_limits() -> None:
    m = Method('&-1-1-1,2', 6)

    with pytest.raises(ValueError):
        m.is_symmetric(-1)

    m.is_symmetric(0)
    m.is_symmetric(5)

    with pytest.raises(IndexError):
        m.is_symmetric(6)


def test_is_palindromic_limits() -> None:
    m = Method('&-1-1-1,2', 6)

    with pytest.raises(ValueError):
        m.is_palindromic(-1)

    m.is_palindromic(0)
    m.is_palindromic(5)

    with pytest.raises(IndexError):
        m.is_palindromic(6)


def test_is_plain_limits() -> None:
    m = Method('&-1-1-1,2', 6)

    with pytest.raises(ValueError):
        m.is_plain(-1)

    m.is_plain(0)
    m.is_plain(5)

    with pytest.raises(IndexError):
        m.is_plain(6)


def test_has_dodges_limits() -> None:
    m = Method('&-1-1-1,2', 6)

    with pytest.raises(ValueError):
        m.has_dodges(-1)

    m.has_dodges(0)
    m.has_dodges(5)

    with pytest.raises(IndexError):
        m.has_dodges(6)


def test_has_places_limits() -> None:
    m = Method('&-1-1-1,2', 6)

    with pytest.raises(ValueError):
        m.has_places(-1)

    m.has_places(0)
    m.has_places(5)

    with pytest.raises(IndexError):
        m.has_places(6)


def test_symmetry_point_limits() -> None:
    m = Method('&-1-1-1,2', 6)

    with pytest.raises(ValueError):
        m.symmetry_point(-1)

    m.symmetry_point(0)
    m.symmetry_point(5)

    with pytest.raises(IndexError):
        m.symmetry_point(6)


@pytest.mark.parametrize('method', (
    'is_symmetric',
    'is_palindromic',
    'is_plain',
    'has_dodges',
    'has_places',
    'symmetry_point',
))
@pytest.mark.parametrize('bell', (Bell(0), '1', b'1', 0))
def test_takes_bell_types(method: str, bell: Bell | str | int) -> None:
    m = Method('&-1-1-1,2', 6)

    # Should succeed
    getattr(m, method)(bell)


def test_symmetry_point_assertion() -> None:
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


def test_index_limits() -> None:
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
