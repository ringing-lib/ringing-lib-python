import pytest

from ringing import Bell, Change


class TestChange:
    def test_change_equals(self):
        assert Change() == Change(0, '')
        assert Change(3) == Change(3, '123')
        assert Change(4) == Change(4, '1234')
        assert Change(5, '3') == Change(5, '3')
        assert Change(6, '1') != Change(6, '5')
        assert Change(8, 'X') == Change(8, '-')
        assert Change(6, '-') != Change(8, '-')
        assert Change(6, '-') != Change(8, '78')

    def test_change_copy(self):
        a = Change(6, '12')
        c = Change(a)
        assert a == c

        # Tests involving change::swap() omitted.

    def test_change_invalid(self):
        with pytest.raises(ValueError):
            Change(5, '18')
        with pytest.raises(ValueError):
            Change(5, 'XYZ')
        with pytest.raises(ValueError):
            Change(5, '!$')
        with pytest.raises(ValueError):
            Change(5, '')
        with pytest.raises(ValueError):
            Change(5, '321')
        with pytest.raises(ValueError):
            Change(5, '11')
        with pytest.raises(ValueError):
            Change(5, '12 3')

    def test_change_implicit_places(self):
        assert Change(6, '4') == Change(6, '14')
        assert Change(5, '-') == Change(5, '5')
        assert Change(7, '12') == Change(7, '127')

        with pytest.raises(ValueError):
            Change(5, '15')

    def test_change_set(self):
        a = Change()
        assert a != Change(6, '16')

        a.set(6, '16')
        assert a == Change(6, '16')

    def test_change_reverse(self):
        assert Change(5, '1').reverse() == Change(5, '5')
        assert Change(6, '16').reverse() == Change(6, '16')
        assert Change(8, 'X').reverse() == Change(8, 'X')
        assert Change(4, '12').reverse() == Change(4, '34')

    def test_change_print(self):
        assert str(Change()) == ''
        assert str(Change(8, '-')) == 'X'
        assert str(Change(8, '18')) == '18'
        assert str(Change(10, '18')) == '18'
        assert str(Change(10, '4')) == '14'
        assert str(Change(10, '129')) == '1290'
        assert str(Change(16, 'E')) == 'ED'

    def test_change_bells(self):
        assert Change().bells == 0
        assert Change(7).bells == 7
        assert Change(8, '14').bells == 8

    def test_change_sign(self):
        assert Change().sign() == +1
        assert Change(4).sign() == +1
        assert Change(9).sign() == +1
        assert Change(9, '1').sign() == +1
        assert Change(9, '9').sign() == +1
        assert Change(9, '129').sign() == -1
        assert Change(6, '12').sign() == +1
        assert Change(6, '-').sign() == -1
        assert Change(8, '-').sign() == +1

    def test_change_findswap(self):
        c = Change(12, '145T')
        assert not c.find_swap(0)  # 1-2
        assert c.find_swap(1)  # 2-3
        assert not c.find_swap(2)  # 3-4
        assert not c.find_swap(3)  # 4-5
        assert c.find_swap(5)  # 6-7
        assert not c.find_swap(10)  # E-T

    def test_change_findplace(self):
        c = Change(10, '1230')
        assert c.find_place(0)
        assert c.find_place(1)
        assert c.find_place(2)
        assert not c.find_place(3)
        assert not c.find_place(8)
        assert c.find_place(9)

    def test_change_swappair(self):
        c = Change(8, '-')

        assert not c.swap_pair(0)
        assert c == '12'
        assert c.swap_pair(1)
        assert c == '14'
        assert c.swap_pair(0)
        assert c == '34'
        assert c.swap_pair(2)
        assert c == 'X'

        assert not c.swap_pair(2)
        assert c == '34'
        assert not c.swap_pair(0)
        assert c == '1234'
        assert c.swap_pair(1)
        assert c == '14'
        assert not c.swap_pair(6)
        assert c == '1478'

        with pytest.raises(IndexError):
            c.swap_pair(11)
        with pytest.raises(IndexError):
            c.swap_pair(7)

    def test_change_internal(self):
        assert not Change().internal()
        assert not Change(1).internal()
        assert not Change(2).internal()
        assert Change(3).internal()
        assert not Change(5, '1').internal()
        assert Change(5, '125').internal()
        assert not Change(6, '-').internal()
        assert not Change(6, '16').internal()
        assert Change(6, '1256').internal()
        assert Change(4, '1234').internal()
        assert Change(8, '4').internal()
        assert Change(8, '3').internal()
        assert not Change(8, '1').internal()

    def test_change_count_places(self):
        assert Change(8).count_places() == 8
        assert Change(8, '3').count_places() == 2
        assert Change(8, '6').count_places() == 2
        assert Change(8, '36').count_places() == 2
        assert Change(8, '18').count_places() == 2
        assert Change(8, '78').count_places() == 2
        assert Change(9, '7').count_places() == 1
        assert Change(9, '1').count_places() == 1
        assert Change(9, '9').count_places() == 1

    def test_change_comparison(self):
        assert Change(6, '1234') < Change(8, '56')
        assert Change(6, '1234') <= Change(8, '56')
        assert not Change(6, '1234') > Change(8, '56')
        assert not Change(6, '1234') >= Change(8, '56')

        assert Change(6, '1234') > Change(6, '56')
        assert Change(6, '1234') >= Change(6, '56')
        assert not Change(6, '1234') < Change(6, '56')
        assert not Change(6, '1234') <= Change(6, '56')

        assert not Change(6, 'X') > Change(6, 'X')
        assert Change(6, 'X') >= Change(6, 'X')
        assert not Change(6, 'X') < Change(6, 'X')
        assert Change(6, 'X') <= Change(6, 'X')

        assert Change(6) < Change(6, '3456')
        assert Change(6, '3456') < Change(6, '56')
        assert Change(6, '56') < Change(6, '36')
        assert Change(6, '36') < Change(6, '16')

    def test_change_output(self):
        string = '.'.join(map(str, [
            Change(6, '-'),
            Change(6, '3'),
            Change(6, '-'),
            Change(6, '4'),
        ]))
        assert string == 'X.36.X.14'

    def test_change_many_bells(self):
        n = Bell.MAX_BELLS + 4

        c = Change(n)

        assert not c.find_swap(n - 2)
        assert c.swap_pair(n - 2)

        assert not c.find_place(n - 1)
        assert not c.find_place(n - 2)
        assert c.find_place(n - 3)

        assert c.find_swap(n - 2)
        assert not c.find_swap(n - 3)
        assert not c.find_swap(n - 4)

        assert c.count_places() == n - 2
        assert c.internal()

        assert not c.reverse().find_place(0)
        assert c.reverse().find_place(3)
        assert c.reverse().internal()

    def test_change_multiply_bell(self):
        b1 = 3

        b1 = b1 * Change(6, '-')
        assert b1 == 2
        b1 = b1 * Change(6, '3')
        assert b1 == 2
        b1 = b1 * Change(6, '-')
        assert b1 == 3
        b1 = b1 * Change(6, '4')
        assert b1 == 3
        b1 = b1 * Change(6, '-')
        assert b1 == 2

        b2 = 0

        b2 = b2 * Change(6, '-')
        assert b2 == 1
        b2 = b2 * Change(6, '3')
        assert b2 == 0
        b2 = b2 * Change(6, '-')
        assert b2 == 1
        b2 = b2 * Change(6, '4')
        assert b2 == 2
        b2 = b2 * Change(6, '-')
        assert b2 == 3

        assert b2 * Change(6, '16') == 4
        assert b2 == 3

        assert 10 * Change(4, 'X') == 10
        assert 9 * Change() == 9
