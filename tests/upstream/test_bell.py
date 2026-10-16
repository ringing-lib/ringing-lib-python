import pytest

from ringing import Bell


class TestBell:
    def test_bell(self):
        assert Bell() == 0
        assert Bell(4) == 4
        assert Bell(Bell.MAX_BELLS) == Bell.MAX_BELLS

    def test_bell_from_char(self):
        assert Bell('5') == 4
        assert Bell('0') == 9
        assert Bell('T') == 11

        # Should this be a custom excption?
        with pytest.raises(ValueError):
            Bell('%')

    def test_bell_to_char(self):
        assert Bell(5).to_char() == '6'
        assert Bell(10).to_char() == 'E'
        assert Bell(14).to_char() == 'C'
        assert Bell(Bell.MAX_BELLS).to_char() == '*'

    def test_bell_output(self):
        s = '{0}{1}{2}'.format(Bell(5), Bell(12), Bell(Bell.MAX_BELLS))
        expected = '6A{' + str(Bell.MAX_BELLS + 1) + '}'
        assert s == expected
