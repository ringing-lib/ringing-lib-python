from os import path
import unittest

from row import Row


class RowTest(unittest.TestCase):
    def test_row_equals(self):
        self.assertTrue(Row() == Row(''))
        self.assertTrue(Row() != Row('1'))
        self.assertTrue(Row(6) == Row('123456'))

        self.assertTrue(Row('123456') == Row('123456'))
        self.assertFalse(Row('123456') != Row('123456'))

        self.assertTrue(Row('123456') != Row('123465'))
        self.assertFalse(Row('123456') == Row('123465'))

        self.assertTrue(Row('123456') != Row('1234'))
        self.assertFalse(Row('123456') == Row('1234'))

        self.assertTrue(Row('123456') != Row('12345678'))
        self.assertFalse(Row('123456') == Row('12345678'))

    def test_row_equals_string_types(self):
        self.assertEqual(Row('123456'), '123456')

        self.assertEqual(Row(b'123456'), b'123456')
        self.assertEqual(Row(u'123456'), u'123456')

        self.assertEqual(bytes(Row('123456')), b'123456')

        try:
            self.assertEqual(unicode(Row('123456')), u'123456')
        except NameError:
            pass

    def test_row_invalid(self):
        self.assertRaises(ValueError, lambda: Row('124'))
        self.assertRaises(ValueError, lambda: Row('12#'))
        self.assertRaises(ValueError, lambda: Row('5444'))
        self.assertRaises(ValueError, lambda: Row('098765432'))

    def test_row_multiply_row(self):
        self.assertEqual(Row('4312') * Row('2341'), Row('3124'))
        self.assertEqual(Row('7631425') * Row('2347165'), Row('6315724'))
        self.assertEqual(Row('12387654') * Row('631245'), Row('63128754'))
        self.assertEqual(Row('24531') * Row('57863124'), Row('17865243'))

        r = Row()
        r = r * '34512'
        self.assertEqual(r, '34512')
        r = r * '14253'
        self.assertEqual(r, '31425')

    def test_row_divide_row(self):
        self.assertEqual(Row('642153') / Row('235164'), Row('164325'))
        self.assertEqual(Row('53678421') / Row('425613'), Row('83456721'))
        self.assertEqual(Row('51324') / Row('645231'), Row('624135'))

        r = Row()
        r = r / '623415'
        self.assertEqual(r, '523461')
        r = r / '623415'
        self.assertEqual(r, '623415')
        r = r / '87654321'
        self.assertEqual(r, '87514326')
        self.assertEqual(r.bells, 8)

    def test_row_inverse(self):
        self.assertEqual(Row('654321').inverse(), '654321')
        self.assertEqual(Row('312').inverse(), '231')
        self.assertEqual(Row('18234567').inverse(), '13456782')

    def test_row_inverse_tilde(self):
        self.assertEqual(~Row('654321'), '654321')
        self.assertEqual(~Row('312'), '231')
        self.assertEqual(~Row('18234567'), '13456782')

    def test_row_print(self):
        self.assertEqual(str(Row()), '')
        self.assertEqual(str(Row('123456')), '123456')

    def test_row_bells(self):
        self.assertEqual(Row().bells, 0)
        self.assertEqual(Row(7).bells, 7)
        self.assertEqual(Row('12345').bells, 5)

    def test_row_rounds(self):
        self.assertEqual(Row().make_rounds(), '')
        self.assertEqual(Row('54321').make_rounds(), '12345')
        self.assertEqual(Row('84567123').make_rounds(), Row(8))

        r = Row('54321').make_rounds()
        self.assertEqual(r, '12345')
        r = Row('84567123').make_rounds()
        self.assertEqual(r, '12345678')

    def test_row_named_rows(self):
        self.assertEqual(Row.queens(0), '')
        self.assertEqual(Row.queens(1), '1')
        self.assertEqual(Row.queens(2), '12')
        self.assertEqual(Row.queens(5), '13524')
        self.assertEqual(Row.queens(8), '13572468')

        self.assertEqual(Row.kings(0), '')
        self.assertEqual(Row.kings(1), '1')
        self.assertEqual(Row.kings(2), '12')
        self.assertEqual(Row.kings(5), '53124')
        self.assertEqual(Row.kings(8), '75312468')

        self.assertEqual(Row.tittums(0), '')
        self.assertEqual(Row.tittums(1), '1')
        self.assertEqual(Row.tittums(2), '12')
        self.assertEqual(Row.tittums(5), '14253')
        self.assertEqual(Row.tittums(8), '15263748')

        self.assertEqual(Row.reverse_rounds(0), '')
        self.assertEqual(Row.reverse_rounds(1), '1')
        self.assertEqual(Row.reverse_rounds(2), '21')
        self.assertEqual(Row.reverse_rounds(5), '54321')
        self.assertEqual(Row.reverse_rounds(8), '87654321')

    def test_row_pblh(self):
        self.assertEqual(Row.pblh(0), Row())
        self.assertEqual(Row.pblh(1), Row('1'))
        self.assertEqual(Row.pblh(2), Row('12'))
        self.assertEqual(Row.pblh(3), Row('132'))
        self.assertEqual(Row.pblh(5), Row('13524'))
        self.assertEqual(Row.pblh(6), Row('135264'))

        self.assertEqual(Row.pblh(3, 10), Row('123'))
        self.assertEqual(Row.pblh(3, 2), Row('123'))
        self.assertEqual(Row.pblh(3, 2), Row('123'))
        self.assertEqual(Row.pblh(6, 2), Row('124635'))
        self.assertEqual(Row.pblh(7, 2), Row('1246375'))
        self.assertEqual(Row.pblh(9, 5), Row('123457968'))

    def test_row_cyclic(self):
        self.assertEqual(Row.cyclic(0), Row())
        self.assertEqual(Row.cyclic(1), Row('1'))
        self.assertEqual(Row.cyclic(2), Row('12'))
        self.assertEqual(Row.cyclic(3), Row('132'))
        self.assertEqual(Row.cyclic(5), Row('13452'))
        self.assertEqual(Row.cyclic(8), Row('13456782'))

        self.assertEqual(Row.cyclic(3, 0), Row('231'))
        self.assertEqual(Row.cyclic(3, 2), Row('123'))
        self.assertEqual(Row.cyclic(3, 3), Row('123'))
        self.assertEqual(Row.cyclic(3, 9), Row('123'))
        self.assertEqual(Row.cyclic(8, 0), Row('23456781'))
        self.assertEqual(Row.cyclic(8, 2), Row('12456783'))
        self.assertEqual(Row.cyclic(9, 2), Row('124567893'))

        self.assertEqual(Row.cyclic(8, 1, -1), Row('18234567'))
        self.assertEqual(Row.cyclic(8, 1, 0), Row('12345678'))
        self.assertEqual(Row.cyclic(8, 1, 2), Row('14567823'))
        self.assertEqual(Row.cyclic(8, 1, 5), Row('17823456'))
        self.assertEqual(Row.cyclic(8, 1, 7), Row('12345678'))
        self.assertEqual(Row.cyclic(8, 1, 13), Row('18234567'))

    def test_row_isrounds(self):
        self.assertTrue(Row(0).is_rounds())
        self.assertTrue(Row(1).is_rounds())
        self.assertTrue(Row(2).is_rounds())

        self.assertTrue(Row('12345678').is_rounds())
        self.assertFalse(Row('21').is_rounds())

    def test_row_ispblh(self):
        # TODO: more tests needed here.
        self.assertTrue(Row('135264').is_pblh())
        self.assertTrue(Row('156342').is_pblh())
        self.assertFalse(Row('165342').is_pblh())

        self.assertTrue(Row('1246375').is_pblh())
        self.assertTrue(Row('1267453').is_pblh())
        self.assertFalse(Row('1267543').is_pblh())

    def test_row_sign(self):
        self.assertEqual(Row().sign(), +1)
        self.assertEqual(Row(1).sign(), +1)
        self.assertEqual(Row(2).sign(), +1)
        self.assertEqual(Row(17).sign(), +1)

        self.assertEqual(Row('234561').sign(), -1)
        self.assertEqual(Row('234516').sign(), +1)
        self.assertEqual(Row('352461').sign(), +1)

        self.assertEqual(Row('312647958').sign(), -1)
        self.assertEqual(Row('167832495').sign(), +1)

    def test_row_cycles(self):
        self.assertEqual(Row().cycles(), '')
        self.assertEqual(Row(1).cycles(), '1')
        self.assertEqual(Row(5).cycles(), '1,2,3,4,5')
        self.assertEqual(Row('124536').cycles(), '1,2,345,6')
        self.assertEqual(Row('214563').cycles(), '12,3456')
        self.assertEqual(Row('2145673').cycles(), '12,34567')

    def test_row_order(self):
        self.assertEqual(Row().order(), 1)
        self.assertEqual(Row(1).order(), 1)
        self.assertEqual(Row('21').order(), 2)
        self.assertEqual(Row('234561').order(), 6)
        self.assertEqual(Row('21436578').order(), 2)
        self.assertEqual(Row('2315674').order(), 12)

    def test_row_comparison(self):
        self.assertTrue(Row('654321') > Row(8))
        self.assertTrue(Row('654321') >= Row(8))
        self.assertFalse(Row('654321') < Row(8))
        self.assertFalse(Row('654321') <= Row(8))

        self.assertTrue(Row('654321') > Row(6))
        self.assertTrue(Row('654321') >= Row(6))
        self.assertFalse(Row('654321') < Row(6))
        self.assertFalse(Row('654321') <= Row(6))

        self.assertFalse(Row('1432') > Row('1432'))
        self.assertTrue(Row('1432') >= Row('1432'))
        self.assertFalse(Row('1432') < Row('1432'))
        self.assertTrue(Row('1432') <= Row('1432'))

        self.assertTrue(Row('1234') < Row('1243'))
        self.assertTrue(Row('1243') < Row('1432'))
        self.assertTrue(Row('1432') < Row('4312'))
