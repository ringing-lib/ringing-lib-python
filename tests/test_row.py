import itertools
import pytest

from ringing import Bell, Row
from tests import MAX_BELL_NUMBER


def test_constructor_bad_input_type() -> None:
    with pytest.raises(TypeError):
        Row([])


def test_bell_number_range() -> None:
    with pytest.raises(ValueError):
        Row(-1)

    Row(0)
    Row(MAX_BELL_NUMBER)

    with pytest.raises(ValueError):
        Row(MAX_BELL_NUMBER + 1)


@pytest.mark.parametrize('self, other', (
    ('123456', '123456'),
    ('123456', b'123456'),
    (b'123456', '123456'),
    (b'123456', b'123456'),
))
def test_equals_string_types(self: str | bytes, other: str | bytes) -> None:
    assert Row(self) == other
    assert other == Row(self)


@pytest.mark.parametrize('input, expected', (
    (Bell(0), 1),
    (Bell('1'), 1),
    (0, 1),
    (1, 4),
    (2, 5),
    (3, 3),
    (4, 2),
    (5, 0),
    (6, 6),
))
def test_find(input: Bell | int, expected: int) -> None:
    r = Row('615423')
    assert r.find(input) == expected


def test_find_bell_range() -> None:
    r = Row('615423')

    with pytest.raises(ValueError):
        r.find(-1)

    r.find(0)
    r.find(MAX_BELL_NUMBER)

    with pytest.raises(ValueError):
        r.find(MAX_BELL_NUMBER + 1)


def test_conjugator() -> None:
    x = Row('2143')
    y = Row('3412')

    r = Row.conjugator(x, y)
    assert y == ~r * x * r

    assert not Row.conjugator(x, 4)


def test_are_conjugate() -> None:
    conj_class = list(map(Row, ['2143', '3412', '4321']))

    for r1, r2 in itertools.product(conj_class, conj_class):
        assert Row.are_conjugate(r1, r2)

    for r in conj_class:
        assert not Row.are_conjugate(r, 4)


OPERATORS = (
    '__lt__',
    '__le__',
    '__eq__',
    '__ne__',
    '__gt__',
    '__ge__',
    '__mul__',
    '__rmul__',
    '__truediv__',
    '__rtruediv__',
)


@pytest.mark.parametrize('operator', OPERATORS)
def test_operators_return_not_implemented_for_unknown_types(operator) -> None:
    assert getattr(Row(), operator)([]) == NotImplemented


@pytest.mark.parametrize('operator', OPERATORS)
def test_operators_raise_value_error_if_input_not_parsed(operator) -> None:
    with pytest.raises(ValueError):
        getattr(Row(), operator)('!')


@pytest.mark.parametrize('input, expected', (
    (None, 'Row()'),
    ('123456', "Row('123456')"),
))
def test_repr(input: str | None, expected: str) -> None:
    assert repr(Row(input)) == expected


@pytest.mark.parametrize('input, expected', (
    ('654321', '654321'),
    ('312', '231'),
    ('18234567', '13456782'),
))
def test_inverse_tilde(input: str, expected: str) -> None:
    assert ~Row(input) == expected


def test_subscript_returns_bell() -> None:
    r = Row(6)
    assert type(r[0]) == Bell


def test_subscript_bounds() -> None:
    r = Row(6)

    with pytest.raises(IndexError):
        r[-1]

    assert r[0] == 0
    assert r[5] == 5

    with pytest.raises(IndexError):
        r[6]
