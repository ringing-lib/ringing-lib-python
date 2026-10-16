import pytest

from ringing import Bell, Change
from tests import MAX_BELL_NUMBER


def test_constructor_bad_input_type() -> None:
    with pytest.raises(TypeError):
        Change([])
    with pytest.raises(TypeError):
        Change(1, [])


def test_bell_number_range() -> None:
    with pytest.raises(ValueError):
        Change(-1)

    Change(0)
    Change(MAX_BELL_NUMBER)

    with pytest.raises(ValueError):
        Change(MAX_BELL_NUMBER + 1)


@pytest.mark.parametrize('self, other', (
    ('16', '16'),
    ('16', b'16'),
    (b'16', '16'),
    (b'16', b'16'),
))
def test_equals_string_types(self: str | bytes, other: str | bytes) -> None:
    assert Change(6, self) == other
    assert other == Change(6, self)


def test_set_exceptions() -> None:
    c = Change()

    with pytest.raises(ValueError):
        c.set(-1, 'X')
    c.set(0, 'X')
    c.set(MAX_BELL_NUMBER, 'X')
    with pytest.raises(ValueError):
        c.set(MAX_BELL_NUMBER + 1, 'X')

    with pytest.raises(TypeError):
        c.set([], 'X')
    with pytest.raises(TypeError):
        c.set(1, [])

    with pytest.raises(ValueError):
        Change(5, 'XYZ')


def test_set_returns_none() -> None:
    c = Change()
    assert c.set(4, 'X') is None


def test_index_method_bounds() -> None:
    c = Change(6)

    with pytest.raises(ValueError):
        c.find_swap(-1)
    assert not c.find_swap(0)
    assert not c.find_swap(4)
    with pytest.raises(IndexError):
        c.find_swap(5)

    with pytest.raises(ValueError):
        c.find_place(-1)
    assert c.find_place(0)
    assert c.find_place(5)
    with pytest.raises(IndexError):
        c.find_place(6)

    with pytest.raises(ValueError):
        c.swap_pair(-1)
    assert c.swap_pair(0)
    assert c.swap_pair(4)
    with pytest.raises(IndexError):
        c.swap_pair(5)


def test_index_method_types() -> None:
    c = Change(6)

    c.find_swap(Bell(0))
    c.find_swap('1')
    c.find_swap(0)

    c.find_place(Bell(0))
    c.find_place('1')
    c.find_place(0)

    c.swap_pair(Bell(0))
    c.swap_pair('1')
    c.swap_pair(0)

    with pytest.raises(TypeError):
        c.find_swap([])
    with pytest.raises(TypeError):
        c.find_place([])
    with pytest.raises(TypeError):
        c.swap_pair([])


OPERATORS = (
    '__lt__',
    '__le__',
    '__eq__',
    '__ne__',
    '__gt__',
    '__ge__',
)


@pytest.mark.parametrize('operator', (*OPERATORS, '__mul__', '__rmul__'))
def test_operators_return_not_implemented_for_unknown_types(operator) -> None:
    assert getattr(Change(), operator)([]) == NotImplemented


@pytest.mark.parametrize('operator', OPERATORS)
def test_operators_raise_value_error_if_input_not_parsed(operator) -> None:
    with pytest.raises(ValueError):
        getattr(Change(), operator)('!')


@pytest.mark.parametrize('input, expected', (
    ((None,), 'Change()'),
    ((4,), "Change(4, '1234')"),
    ((4, 'X'), "Change(4, 'X')"),
))
def test_repr(input: tuple, expected: str) -> None:
    assert repr(Change(*input)) == expected


@pytest.mark.parametrize('other, expected', (
    (0, 0),
    (1, 2),
    (2, 1),
    (3, 3),
    (4, 5),
))
def test_bell_multiply_order(other: int, expected: int) -> None:
    c = Change(6, '14')

    assert other * c == expected
    assert c * other == expected


def test_bell_multiply_bounds() -> None:
    c = Change(6, '14')

    with pytest.raises(ValueError):
        c * -1

    c * 0
    c * MAX_BELL_NUMBER

    with pytest.raises(ValueError):
        c * (MAX_BELL_NUMBER + 1)

    with pytest.raises(ValueError):
        -1 * c

    0 * c
    MAX_BELL_NUMBER * c

    with pytest.raises(ValueError):
        (MAX_BELL_NUMBER + 1) * c


def test_bell_multiply_types() -> None:
    c = Change(6, '14')

    c * Bell(0)
    c * '1'
    c * 0

    Bell(0) * c
    '1' * c
    0 * c

    with pytest.raises(TypeError):
        c * []
    with pytest.raises(TypeError):
        [] * c
