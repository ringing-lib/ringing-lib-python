
from ringing import Method


class TestMethod:
    def test_method_equals(self):
        assert Method() == Method(0, 6, 'name')
        assert Method() == Method('', 9)
        assert Method('-', 6) != Method('-', 4)
        assert Method('&-12,1', 8) == Method('+ -12-18', 8)

    def test_method_name(self):
        assert Method('&-12,1', 8).name == 'Untitled'
        assert Method('&-12,1', 8, 'Bastow').name == 'Bastow'

        m = Method('&-12,1', 8)
        m.name = 'Bastow'
        assert m.name == 'Bastow'

        # Skipped identical test setting name from string rather than char *

    def test_method_fullname(self):
        assert Method('&-12,1', 8, 'Bastow').full_name() == 'Bastow Little Bob Major'

        assert Method('&34.1.5.1.5,2', 5,
                   'Reverse Canterbury Pleasure').full_name() == 'Reverse Canterbury Pleasure Place Doubles'

        assert Method('3.1', 3, 'Original').full_name() == 'Original Singles'

        assert Method('&-5-4.5-5.36.4-4.5-4-1,8', 8, 'Bristol').full_name() == 'Bristol Surprise Major'

        assert Method('-', 8, 'Cross').full_name() == 'Cross Major'

        assert Method('-4-6-6-4-6-6-2', 6, "Tetley's Smoothflow").full_name() == "Tetley's Smoothflow Differential Minor"

    def test_method_fullname_grandsire(self):
        assert Method('3,&1-1-1-', 6, 'Grandsire').full_name() == 'Grandsire Minor'

        assert Method('6,&1-1-1.4', 6, 'Reverse Grandsire').full_name() == 'Reverse Grandsire Minor'

        assert Method('3,&1-1-1.4', 6, 'Double Grandsire').full_name() == 'Double Grandsire Minor'

        assert Method('+3,&1.9.1.5.1', 9, 'Little Grandsire').full_name() == 'Little Grandsire Caters'

        assert Method('+3.1.7.1.7.1.7.1.7.1.7.1.5.1', 7, 'Union').full_name() == 'Union Triples'

    def test_method_stagename(self):
        assert Method.stage_name(0) == '0'  # ???
        assert Method.stage_name(1) == '1'
        assert Method.stage_name(2) == '2'

        assert Method.stage_name(3) == 'Singles'
        assert Method.stage_name(4) == 'Minimus'
        assert Method.stage_name(5) == 'Doubles'
        assert Method.stage_name(6) == 'Minor'
        assert Method.stage_name(7) == 'Triples'
        assert Method.stage_name(8) == 'Major'
        assert Method.stage_name(9) == 'Caters'
        assert Method.stage_name(10) == 'Royal'
        assert Method.stage_name(11) == 'Cinques'
        assert Method.stage_name(12) == 'Maximus'
        assert Method.stage_name(13) == 'Sextuples'
        assert Method.stage_name(14) == 'Fourteen'
        assert Method.stage_name(15) == 'Septuples'
        assert Method.stage_name(16) == 'Sixteen'
        assert Method.stage_name(17) == 'Octuples'
        assert Method.stage_name(18) == 'Eighteen'
        assert Method.stage_name(19) == 'Nonuples'
        assert Method.stage_name(20) == 'Twenty'
        assert Method.stage_name(21) == 'Decuples'
        assert Method.stage_name(22) == 'Twenty-two'

        assert Method.stage_name(54) == '54'

    # test_method_classname omitted: not implemented

    def test_method_length(self):
        assert Method('&-12,16', 6).length == 4
        assert Method('&-12,16', 6).size == 4
        assert Method().size == 0

    def test_method_bells(self):
        assert Method('', 6).bells == 6
        assert Method('&-1-1-1,2', 6).bells == 6

    def test_method_lh(self):
        assert Method().lead_head() == ''
        assert Method('&-1-1-1-1,2', 8).lead_head() == '13527486'
        assert Method('&-1-1-1-1,1', 8).lead_head() == '12345678'
        assert Method('&-3-4-2-3-4-5,2', 6).lead_head() == '156342'
        assert Method('+5.3.1.3.1.3', 5).lead_head() == '24153'

    def test_method_issym(self):
        assert Method().is_symmetric()
        assert Method('&-1-1-1,2', 6).is_symmetric()
        assert Method('&-1-1-1,1', 6).is_symmetric()
        assert not Method('3,&1-1-1-', 6).is_symmetric()
        assert not Method('3.1.5.1.5.1.5.1.5.123', 5).is_symmetric()
        assert Method('&-4-36-5-1,8', 8).is_symmetric()
        assert not Method('+5.3.1.3.1.3', 5).is_symmetric()
