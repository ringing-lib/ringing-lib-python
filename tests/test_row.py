import itertools
import pytest

from ringing import Bell, Row
from tests import MAX_BELL_NUMBER


class TestRow:
    def test_row_constructor_exceptions(self):
        with pytest.raises(ValueError):
            Row(-1)
        Row(0)
        Row(MAX_BELL_NUMBER)
        with pytest.raises(ValueError):
            Row(MAX_BELL_NUMBER + 1)
        with pytest.raises(TypeError):
            Row(self)

    def test_row_equals_string_types(self):
        assert Row('123456') == '123456'

        assert Row(b'123456') == b'123456'
        assert Row(u'123456') == u'123456'

        assert bytes(Row('123456')) == b'123456'

        try:
            assert unicode(Row('123456')) == u'123456'
        except NameError:
            pass

    def test_row_find(self):
        r = Row('615423')

        assert r.find(0) == 1
        assert r.find(1) == 4
        assert r.find(2) == 5
        assert r.find(3) == 3
        assert r.find(4) == 2
        assert r.find(5) == 0
        assert r.find(6) == 6

        with pytest.raises(ValueError):
            r.find(-1)
        r.find(0)
        r.find(MAX_BELL_NUMBER)
        with pytest.raises(ValueError):
            r.find(MAX_BELL_NUMBER + 1)
        with pytest.raises(TypeError):
            r.find(self)

        assert r.find(Bell(0)) == 1
        assert r.find(Bell('1')) == 1

    def test_row_conjugator(self):
        x = Row('2143')
        y = Row('3412')

        r = Row.conjugator(x, y)
        assert y == ~r * x * r

        assert not Row.conjugator(x, 4)

    def test_row_are_conjugate(self):
        conj_class = list(map(Row, ['2143', '3412', '4321']))

        for r1, r2 in itertools.product(conj_class, conj_class):
            assert Row.are_conjugate(r1, r2)

        for r in conj_class:
            assert not Row.are_conjugate(r, 4)

    def test_operators_return_not_implemented(self):
        # Arithmetic operator returns NotImplemented when given unknown types
        assert Row().__lt__(self) == NotImplemented
        assert Row().__le__(self) == NotImplemented
        assert Row().__eq__(self) == NotImplemented
        assert Row().__ne__(self) == NotImplemented
        assert Row().__gt__(self) == NotImplemented
        assert Row().__ge__(self) == NotImplemented
        assert Row().__mul__(self) == NotImplemented
        assert Row().__rmul__(self) == NotImplemented
        assert Row().__truediv__(self) == NotImplemented
        assert Row().__rtruediv__(self) == NotImplemented

        # ... but passes through errors parsing known types.
        with pytest.raises(ValueError):
            Row().__lt__('!')
        with pytest.raises(ValueError):
            Row().__le__('!')
        with pytest.raises(ValueError):
            Row().__eq__('!')
        with pytest.raises(ValueError):
            Row().__ne__('!')
        with pytest.raises(ValueError):
            Row().__gt__('!')
        with pytest.raises(ValueError):
            Row().__ge__('!')
        with pytest.raises(ValueError):
            Row().__mul__('!')
        with pytest.raises(ValueError):
            Row().__rmul__('!')
        with pytest.raises(ValueError):
            Row().__truediv__('!')
        with pytest.raises(ValueError):
            Row().__rtruediv__('!')

        try:
            assert Row().__div__(self) == NotImplemented
            with pytest.raises(ValueError):
                Row().__div__('!')
        except AttributeError:
            pass  # Ignore (Python 3 doesn't create __div__)

    def test_row_repr(self):
        assert repr(Row()) == 'Row()'
        assert repr(Row('123456')) == "Row('123456')"

    def test_row_inverse_tilde(self):
        assert ~Row('654321') == '654321'
        assert ~Row('312') == '231'
        assert ~Row('18234567') == '13456782'

    def test_row_subscript_returns_bell(self):
        r = Row(6)
        assert type(r[0]) == Bell

    def test_row_subscript_bounds(self):
        r = Row(6)
        with pytest.raises(IndexError):
            r[-1]
        assert r[0] == 0
        assert r[5] == 5
        with pytest.raises(IndexError):
            r[6]
