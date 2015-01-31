import unittest

from ringing import Method


class MethodTest(unittest.TestCase):
    def test_method_equals(self):
        self.assertTrue(Method() == Method(0, 6, 'name'))
        self.assertTrue(Method() == Method('', 9))
        self.assertTrue(Method('-', 6) != Method('-', 4))
        self.assertTrue(Method('&-12,1', 8) == Method('+ -12-18', 8))

    def test_method_name(self):
        self.assertEqual(Method('&-12,1', 8).name, 'Untitled')
        self.assertEqual(Method('&-12,1', 8, 'Bastow').name, 'Bastow')

        m = Method('&-12,1', 8)
        m.name = 'Bastow'
        self.assertEqual(m.name, 'Bastow')

        # Skipped identical test setting name from string rather than char *

    def test_method_fullname(self):
        self.assertEqual(
            Method('&-12,1', 8, 'Bastow').full_name(),
            'Bastow Little Bob Major'
        )

        self.assertEqual(
            Method('&34.1.5.1.5,2', 5,
                   'Reverse Canterbury Pleasure').full_name(),
            'Reverse Canterbury Pleasure Place Doubles'
        )

        self.assertEqual(
            Method('3.1', 3, 'Original').full_name(),
            'Original Singles'
        )

        self.assertEqual(
            Method('&-5-4.5-5.36.4-4.5-4-1,8', 8, 'Bristol').full_name(),
            'Bristol Surprise Major'
        )

        self.assertEqual(
            Method('-', 8, 'Cross').full_name(),
            'Cross Differential Major'
        )

        self.assertEqual(
            Method('-4-6-6-4-6-6-2', 6, "Tetley's Smoothflow").full_name(),
            "Tetley's Smoothflow Differential Hybrid Minor"
        )

    def test_method_fullname_grandsire(self):
        self.assertEqual(
            Method('3,&1-1-1-', 6, 'Grandsire').full_name(),
            'Grandsire Minor'
        )

        self.assertEqual(
            Method('6,&1-1-1.4', 6, 'Reverse Grandsire').full_name(),
            'Reverse Grandsire Minor'
        )

        self.assertEqual(
            Method('3,&1-1-1.4', 6, 'Double Grandsire').full_name(),
            'Double Grandsire Minor'
        )

        self.assertEqual(
            Method('+3,&1.9.1.5.1', 9, 'Little Grandsire').full_name(),
            'Little Grandsire Caters'
        )

        self.assertEqual(
            Method('+3.1.7.1.7.1.7.1.7.1.7.1.5.1', 7, 'Union').full_name(),
            'Union Triples'
        )

    def test_method_stagename(self):
        self.assertEqual(Method.stage_name(0), '0')  # ???
        self.assertEqual(Method.stage_name(1), '1')
        self.assertEqual(Method.stage_name(2), '2')

        self.assertEqual(Method.stage_name(3), 'Singles')
        self.assertEqual(Method.stage_name(4), 'Minimus')
        self.assertEqual(Method.stage_name(5), 'Doubles')
        self.assertEqual(Method.stage_name(6), 'Minor')
        self.assertEqual(Method.stage_name(7), 'Triples')
        self.assertEqual(Method.stage_name(8), 'Major')
        self.assertEqual(Method.stage_name(9), 'Caters')
        self.assertEqual(Method.stage_name(10), 'Royal')
        self.assertEqual(Method.stage_name(11), 'Cinques')
        self.assertEqual(Method.stage_name(12), 'Maximus')
        self.assertEqual(Method.stage_name(13), 'Sextuples')
        self.assertEqual(Method.stage_name(14), 'Fourteen')
        self.assertEqual(Method.stage_name(15), 'Septuples')
        self.assertEqual(Method.stage_name(16), 'Sixteen')
        self.assertEqual(Method.stage_name(17), 'Octuples')
        self.assertEqual(Method.stage_name(18), 'Eighteen')
        self.assertEqual(Method.stage_name(19), 'Nonuples')
        self.assertEqual(Method.stage_name(20), 'Twenty')
        self.assertEqual(Method.stage_name(21), 'Decuples')
        self.assertEqual(Method.stage_name(22), 'Twenty-two')

        self.assertEqual(Method.stage_name(54), '54')

    # test_method_classname omitted: not implemented

    def test_method_length(self):
        self.assertEqual(Method('&-12,16', 6).length, 4)
        self.assertEqual(Method('&-12,16', 6).size, 4)
        self.assertEqual(Method().size, 0)

    def test_method_bells(self):
        self.assertEqual(Method('', 6).bells, 6)
        self.assertEqual(Method('&-1-1-1,2', 6).bells, 6)

    def test_method_lh(self):
        self.assertEqual(Method().lead_head(), '')
        self.assertEqual(Method('&-1-1-1-1,2', 8).lead_head(), '13527486')
        self.assertEqual(Method('&-1-1-1-1,1', 8).lead_head(), '12345678')
        self.assertEqual(Method('&-3-4-2-3-4-5,2', 6).lead_head(), '156342')
        self.assertEqual(Method('+5.3.1.3.1.3', 5).lead_head(), '24153')

    def test_method_issym(self):
        self.assertTrue(Method().is_symmetric())
        self.assertTrue(Method('&-1-1-1,2', 6).is_symmetric())
        self.assertTrue(Method('&-1-1-1,1', 6).is_symmetric())
        self.assertFalse(Method('3,&1-1-1-', 6).is_symmetric())
        self.assertFalse(Method('3.1.5.1.5.1.5.1.5.123', 5).is_symmetric())
        self.assertTrue(Method('&-4-36-5-1,8', 8).is_symmetric())
        self.assertFalse(Method('+5.3.1.3.1.3', 5).is_symmetric())
