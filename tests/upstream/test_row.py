import pytest

from ringing import Row, Change


class TestRow:
    def test_row_equals(self):
        assert Row() == Row('')
        assert Row() != Row('1')
        assert Row(6) == Row('123456')

        assert Row('123456') == Row('123456')
        assert not Row('123456') != Row('123456')

        assert Row('123456') != Row('123465')
        assert not Row('123456') == Row('123465')

        assert Row('123456') != Row('1234')
        assert not Row('123456') == Row('1234')

        assert Row('123456') != Row('12345678')
        assert not Row('123456') == Row('12345678')

    def test_row_copy(self):
        a = Row('123654')
        c = Row(a)
        assert a == c

        # Tests involving row::swap() omitted.

    def test_row_invalid(self):
        with pytest.raises(ValueError):
            Row('124')
        with pytest.raises(ValueError):
            Row('12#')
        with pytest.raises(ValueError):
            Row('5444')
        with pytest.raises(ValueError):
            Row('098765432')

    def test_row_subscript(self):
        assert Row('1')[0] == 0
        assert Row('15234')[0] == 0
        assert Row('15234')[2] == 1
        assert Row('15234')[4] == 3
        assert Row(12)[11] == 11

    def test_row_multiply_row(self):
        assert Row('4312') * Row('2341') == Row('3124')
        assert Row('7631425') * Row('2347165') == Row('6315724')
        assert Row('12387654') * Row('631245') == Row('63128754')
        assert Row('24531') * Row('57863124') == Row('17865243')

        r = Row()
        r = r * '34512'
        assert r == '34512'
        r = r * '14253'
        assert r == '31425'

    def test_row_divide_row(self):
        assert Row('642153') / Row('235164') == Row('164325')
        assert Row('53678421') / Row('425613') == Row('83456721')
        assert Row('51324') / Row('645231') == Row('624135')

        r = Row()
        r = r / '623415'
        assert r == '523461'
        r = r / '623415'
        assert r == '623415'
        r = r / '87654321'
        assert r == '87514326'
        assert r.bells == 8

    def test_row_multiply_change(self):
        r = Row()
        r = r * Change(6, 'X')
        assert r == '214365'
        r = r * Change(6, '1')
        assert r == '241635'
        r = r * Change(8, 'X')
        assert r == '42615387'
        r = r * Change(5, '3')
        assert r == '24651387'

    def test_row_inverse(self):
        assert Row('654321').inverse() == '654321'
        assert Row('312').inverse() == '231'
        assert Row('18234567').inverse() == '13456782'

    def test_row_print(self):
        assert str(Row()) == ''
        assert str(Row('123456')) == '123456'

        # Tests involving stream operators omitted.

    def test_row_bells(self):
        assert Row().bells == 0
        assert Row(7).bells == 7
        assert Row('12345').bells == 5

    # test_row_rounds omitted as Row objects are immutable.

    def test_row_named_rows(self):
        assert Row.rounds(0) == ''
        assert Row.rounds(1) == '1'
        assert Row.rounds(2) == '12'
        assert Row.rounds(5) == '12345'
        assert Row.rounds(8) == '12345678'

        assert Row.queens(0) == ''
        assert Row.queens(1) == '1'
        assert Row.queens(2) == '12'
        assert Row.queens(5) == '13524'
        assert Row.queens(8) == '13572468'

        assert Row.kings(0) == ''
        assert Row.kings(1) == '1'
        assert Row.kings(2) == '12'
        assert Row.kings(5) == '53124'
        assert Row.kings(8) == '75312468'

        assert Row.tittums(0) == ''
        assert Row.tittums(1) == '1'
        assert Row.tittums(2) == '12'
        assert Row.tittums(5) == '14253'
        assert Row.tittums(8) == '15263748'

        assert Row.reverse_rounds(0) == ''
        assert Row.reverse_rounds(1) == '1'
        assert Row.reverse_rounds(2) == '21'
        assert Row.reverse_rounds(5) == '54321'
        assert Row.reverse_rounds(8) == '87654321'

    def test_row_pblh(self):
        assert Row.pblh(0) == Row()
        assert Row.pblh(1) == Row('1')
        assert Row.pblh(2) == Row('12')
        assert Row.pblh(3) == Row('132')
        assert Row.pblh(5) == Row('13524')
        assert Row.pblh(6) == Row('135264')

        assert Row.pblh(3, 10) == Row('123')
        assert Row.pblh(3, 2) == Row('123')
        assert Row.pblh(3, 2) == Row('123')
        assert Row.pblh(6, 2) == Row('124635')
        assert Row.pblh(7, 2) == Row('1246375')
        assert Row.pblh(9, 5) == Row('123457968')

    def test_row_cyclic(self):
        assert Row.cyclic(0) == Row()
        assert Row.cyclic(1) == Row('1')
        assert Row.cyclic(2) == Row('12')
        assert Row.cyclic(3) == Row('132')
        assert Row.cyclic(5) == Row('13452')
        assert Row.cyclic(8) == Row('13456782')

        assert Row.cyclic(3, 0) == Row('231')
        assert Row.cyclic(3, 2) == Row('123')
        assert Row.cyclic(3, 3) == Row('123')
        assert Row.cyclic(3, 9) == Row('123')
        assert Row.cyclic(8, 0) == Row('23456781')
        assert Row.cyclic(8, 2) == Row('12456783')
        assert Row.cyclic(9, 2) == Row('124567893')

        assert Row.cyclic(8, 1, -1) == Row('18234567')
        assert Row.cyclic(8, 1, 0) == Row('12345678')
        assert Row.cyclic(8, 1, 2) == Row('14567823')
        assert Row.cyclic(8, 1, 5) == Row('17823456')
        assert Row.cyclic(8, 1, 7) == Row('12345678')
        assert Row.cyclic(8, 1, 13) == Row('18234567')

    def test_row_isrounds(self):
        assert Row(0).is_rounds()
        assert Row(1).is_rounds()
        assert Row(2).is_rounds()

        assert Row('12345678').is_rounds()
        assert not Row('21').is_rounds()

    def test_row_ispblh(self):
        assert Row.pblh(0).is_pblh() == 1
        assert Row.pblh(3).is_pblh() == 1
        assert Row.pblh(6).is_pblh() == 1
        assert Row.pblh(9).is_pblh() == 1

        assert Row.rounds(0).is_pblh()
        assert not Row.rounds(1).is_pblh()
        assert not Row.rounds(2).is_pblh()
        assert not Row.rounds(3).is_pblh()
        assert not Row.rounds(6).is_pblh()
        assert not Row.rounds(9).is_pblh()

        assert Row('135264').is_pblh()
        assert Row('156342').is_pblh()
        assert not Row('165342').is_pblh()

        assert Row('1246375').is_pblh()
        assert Row('1267453').is_pblh()
        assert not Row('1267543').is_pblh()

        r = Row.pblh(10)
        assert (r * r * r).is_pblh()

    def test_row_sign(self):
        assert Row().sign() == +1
        assert Row(1).sign() == +1
        assert Row(2).sign() == +1
        assert Row(17).sign() == +1

        assert Row('234561').sign() == -1
        assert Row('234516').sign() == +1
        assert Row('352461').sign() == +1

        assert Row('312647958').sign() == -1
        assert Row('167832495').sign() == +1

    def test_row_cycles(self):
        assert Row().cycles() == ''
        assert Row(1).cycles() == '1'
        assert Row(5).cycles() == '1,2,3,4,5'
        assert Row('124536').cycles() == '1,2,345,6'
        assert Row('214563').cycles() == '12,3456'
        assert Row('2145673').cycles() == '12,34567'

    def test_row_order(self):
        assert Row().order() == 1
        assert Row(1).order() == 1
        assert Row('21').order() == 2
        assert Row('234561').order() == 6
        assert Row('21436578').order() == 2
        assert Row('2315674').order() == 12

    def test_row_comparison(self):
        assert Row('654321') > Row(8)
        assert Row('654321') >= Row(8)
        assert not Row('654321') < Row(8)
        assert not Row('654321') <= Row(8)

        assert Row('654321') > Row(6)
        assert Row('654321') >= Row(6)
        assert not Row('654321') < Row(6)
        assert not Row('654321') <= Row(6)

        assert not Row('1432') > Row('1432')
        assert Row('1432') >= Row('1432')
        assert not Row('1432') < Row('1432')
        assert Row('1432') <= Row('1432')

        assert Row('1234') < Row('1243')
        assert Row('1243') < Row('1432')
        assert Row('1432') < Row('4312')
