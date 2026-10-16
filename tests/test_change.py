import pytest

from ringing import Bell, Change
from tests import MAX_BELL_NUMBER


class TestChange:
    def test_change_constructor_exceptions(self):
        with pytest.raises(ValueError):
            Change(-1)
        Change(0)
        Change(MAX_BELL_NUMBER)
        with pytest.raises(ValueError):
            Change(MAX_BELL_NUMBER + 1)

        with pytest.raises(TypeError):
            Change(self)
        with pytest.raises(TypeError):
            Change(1, self)

    def test_change_equals_string_types(self):
        assert Change(6, '16') == '16'

        assert Change(6, b'16') == b'16'
        assert Change(6, u'16') == u'16'

        assert bytes(Change(6, '16')) == b'16'

        try:
            assert unicode(Change(6, '16')) == u'16'
        except NameError:
            pass

    def test_change_set_exceptions(self):
        c = Change()

        with pytest.raises(ValueError):
            c.set(-1, 'X')
        c.set(0, 'X')
        c.set(MAX_BELL_NUMBER, 'X')
        with pytest.raises(ValueError):
            c.set(MAX_BELL_NUMBER + 1, 'X')

        with pytest.raises(TypeError):
            c.set(self, 'X')
        with pytest.raises(TypeError):
            c.set(1, self)

        with pytest.raises(ValueError):
            Change(5, 'XYZ')

    def test_change_set_returns_none(self):
        c = Change()
        assert c.set(4, 'X') == None

    def test_index_method_bounds(self):
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

    def test_index_method_types(self):
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
            c.find_swap(self)
        with pytest.raises(TypeError):
            c.find_place(self)
        with pytest.raises(TypeError):
            c.swap_pair(self)

    def test_operators_return_not_implemented(self):
        # Arithmetic operator returns NotImplemented when given unknown types
        assert Change().__lt__(self) == NotImplemented
        assert Change().__le__(self) == NotImplemented
        assert Change().__eq__(self) == NotImplemented
        assert Change().__ne__(self) == NotImplemented
        assert Change().__gt__(self) == NotImplemented
        assert Change().__ge__(self) == NotImplemented
        assert Change().__mul__(self) == NotImplemented
        assert Change().__rmul__(self) == NotImplemented

        # ... but passes through errors parsing known types.
        with pytest.raises(ValueError):
            Change().__lt__('!')
        with pytest.raises(ValueError):
            Change().__le__('!')
        with pytest.raises(ValueError):
            Change().__eq__('!')
        with pytest.raises(ValueError):
            Change().__ne__('!')
        with pytest.raises(ValueError):
            Change().__gt__('!')
        with pytest.raises(ValueError):
            Change().__ge__('!')

    def test_change_repr(self):
        assert repr(Change()) == 'Change()'
        assert repr(Change(4)) == "Change(4, '1234')"
        assert repr(Change(4, 'X')) == "Change(4, 'X')"

    @pytest.mark.parametrize('other, expected', (
        (0, 0),
        (1, 2),
        (2, 1),
        (3, 3),
        (4, 5),
    ))
    def test_bell_multiply_order(self, other: int, expected: int):
        c = Change(6, '14')

        assert other * c == expected
        assert c * other == expected

    def test_bell_multiply_bounds(self):
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

    def test_bell_multiply_types(self):
        c = Change(6, '14')

        c * Bell(0)
        c * '1'
        c * 0

        Bell(0) * c
        '1' * c
        0 * c

        with pytest.raises(TypeError):
            c * self
        with pytest.raises(TypeError):
            self * c
