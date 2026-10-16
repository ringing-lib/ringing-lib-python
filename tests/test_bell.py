from collections.abc import Generator
from typing import Any

import pytest

from ringing import Bell
from tests import MAX_BELL_NUMBER


NEW_SYMBOLS = 'abcdef%'


@pytest.fixture
def symbols() -> Generator[None, None, None]:
    Bell.set_symbols(NEW_SYMBOLS)
    yield
    Bell.set_symbols()


def test_constructor_with_none() -> None:
    assert Bell() == Bell(0)


@pytest.mark.parametrize('input', (10, Bell(10), 'e', b'e', 'E', b'E'))
def test_constructor_with_input(input: Any) -> None:
    assert Bell(input) == Bell(10)


@pytest.mark.parametrize('input', (-1, '%', b'%', 'ao', '•', 1.5, []))
def test_invalid_input(input: Any) -> None:
    with pytest.raises((TypeError, ValueError)):
        Bell(input)


def test_bell_number_range() -> None:
    with pytest.raises(ValueError):
        Bell(-1)

    Bell(0)
    Bell(MAX_BELL_NUMBER)

    with pytest.raises(ValueError):
        Bell(MAX_BELL_NUMBER + 1)


@pytest.mark.parametrize('test_type', (bytes, str, int))
def test_type_conversion(test_type: type) -> None:
    assert isinstance(test_type(Bell(5)), test_type)


@pytest.mark.parametrize('symbol', ('1', b'1', 'a', b'a', 'A', b'A'))
def test_is_symbol(symbol: str | bytes) -> None:
    assert Bell.is_symbol(symbol)


@pytest.mark.parametrize('symbol', ('%', b'%'))
def test_is_not_symbol(symbol: str | bytes) -> None:
    assert not Bell.is_symbol(symbol)


def test_repr() -> None:
    assert repr(Bell(5)) == 'Bell(5)'


def test_symbols_set(symbols: Generator[None, None, None]) -> None:
    for index, character in enumerate(NEW_SYMBOLS):
        assert Bell(index) == character


def test_is_new_symbol(symbols: Generator[None, None, None]) -> None:
    for character in NEW_SYMBOLS:
        assert Bell.is_symbol(character)


def test_max_bells(symbols: Generator[None, None, None]) -> None:
    assert Bell.MAX_BELLS == len(NEW_SYMBOLS)


def test_symbols_restored(symbols: Generator[None, None, None]) -> None:
    Bell.set_symbols()
    assert Bell(0).to_char() == '1'
