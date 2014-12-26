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

    def test_row_invalid(self):
        self.assertRaises(ValueError, lambda: Row('124'))
        self.assertRaises(ValueError, lambda: Row('12#'))
        self.assertRaises(ValueError, lambda: Row('5444'))
        self.assertRaises(ValueError, lambda: Row('098765432'))

    def test_row_print(self):
        self.assertEqual(str(Row()), '')
        self.assertEqual(str(Row('123456')), '123456')

    def test_row_bells(self):
        self.assertEqual(Row().bells, 0)
        self.assertEqual(Row(7).bells, 7)
        self.assertEqual(Row('12345').bells, 5)

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
