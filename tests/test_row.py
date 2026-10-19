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


def test_conjugate() -> None:
    s = Row('2143')
    r = Row('3412')
    assert s.conjugate(r) == ~r * s * r


@pytest.mark.parametrize('input, expected', (
    ('', ''),
    ('123456', '1,2,3,4,5,6'),
    ('2143', '12,34'),
    ('135264', '1,23564'),
    ('21453678', '12,345,6,7,8')
))
def test_cycles(input: str, expected: str) -> None:
    assert Row(input).cycles() == expected


@pytest.mark.parametrize('input, expected', (
    ('', 0),
    ('123456', 6),
    ('2143', 2),
    ('135264', 2),
    ('21453678', 5)
))
def test_num_cycles(input: str, expected: int) -> None:
    assert Row(input).num_cycles() == expected


@pytest.mark.parametrize('input, bell, expected', (
    ('123456', '1', 1),
    ('123456', '2', 1),
    ('123456', '3', 1),
    ('123456', '4', 1),
    ('123456', '5', 1),
    ('123456', '6', 1),
    ('2143', '1', 2),
    ('2143', '2', 2),
    ('2143', '3', 2),
    ('2143', '4', 2),
    ('135264', '1', 1),
    ('135264', '2', 5),
    ('135264', '3', 5),
    ('135264', '4', 5),
    ('135264', '5', 5),
    ('135264', '6', 5),
    ('21453678', '1', 2),
    ('21453678', '2', 2),
    ('21453678', '3', 3),
    ('21453678', '4', 3),
    ('21453678', '5', 3),
    ('21453678', '6', 1),
    ('21453678', '7', 1),
    ('21453678', '8', 1),
))
def test_cycle_size(input: str, bell: str, expected: int) -> None:
    assert Row(input).cycle_size(bell) == expected


def test_cycle_size_range() -> None:
    r = Row('123456')

    with pytest.raises(ValueError):
        r.cycle_size(-1)

    r.cycle_size(0)
    r.cycle_size(5)

    with pytest.raises(ValueError):
        r.cycle_size(6)
    with pytest.raises(ValueError):
        r.cycle_size(MAX_BELL_NUMBER)
    with pytest.raises(ValueError):
        r.cycle_size(MAX_BELL_NUMBER + 1)


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
    conj_class = [Row('2143'), Row('3412'), Row('4321')]

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
