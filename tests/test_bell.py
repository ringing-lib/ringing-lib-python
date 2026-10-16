import sys
import pytest

from ringing import Bell
from tests import MAX_BELL_NUMBER


class TestBell:
    def test_bell_constructor(self):
        assert Bell(Bell(10)) == 10
        assert Bell('e') == 10
        assert Bell(u'e') == 10
        assert Bell(b'e') == 10
        assert Bell('E') == 10
        assert Bell(u'E') == 10
        assert Bell(b'E') == 10

    def test_bell_constructor_exceptions(self):
        with pytest.raises(TypeError):
            Bell(self)

        with pytest.raises(ValueError):
            Bell(-1)
        Bell(0)
        Bell(MAX_BELL_NUMBER)
        with pytest.raises(ValueError):
            Bell(MAX_BELL_NUMBER + 1)

        with pytest.raises(ValueError):
            Bell('%')
        with pytest.raises(ValueError):
            Bell(u'%')
        with pytest.raises(ValueError):
            Bell(b'%')

    def test_bell_bytes_bytes(self):
        assert type(bytes(Bell(5))) == bytes

    def test_bell_unicode_unicode(self):
        if sys.version_info[0] < 3:
            assert type(unicode(Bell(5))) == unicode
        else:
            assert type(Bell(5).__unicode__()) == str

    def test_is_symbol(self):
        assert Bell.is_symbol('1')
        assert Bell.is_symbol(u'1')
        assert Bell.is_symbol(b'1')
        assert Bell.is_symbol('a')
        assert Bell.is_symbol(u'a')
        assert Bell.is_symbol(b'a')
        assert Bell.is_symbol('A')
        assert Bell.is_symbol(u'A')
        assert Bell.is_symbol(b'A')

        assert not Bell.is_symbol('%')
        assert not Bell.is_symbol(u'%')
        assert not Bell.is_symbol(b'%')


class TestBellSymbols:
    NEW_SYMBOLS = 'abcdef%'

    def setup_method(self, test_method):
        Bell.set_symbols(self.NEW_SYMBOLS)

    def teardown_method(self, test_method):
        Bell.set_symbols()

    def test_symbols_set(self):
        for index, character in enumerate(self.NEW_SYMBOLS):
            assert Bell(index) == character

    def test_is_symbol(self):
        for character in self.NEW_SYMBOLS:
            assert Bell.is_symbol(character)

    def test_max_bells(self):
        assert Bell.MAX_BELLS == len(self.NEW_SYMBOLS)

    def test_symbols_restored(self):
        Bell.set_symbols()
        assert Bell(0).to_char() == '1'
