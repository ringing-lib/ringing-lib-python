
from ringing import RowBlock, Change


class TestRowBlock:
    def test_row_block_constructors(self):
        changes = []
        changes.append(Change(5, '3'))
        changes.append(Change(5, '1'))
        changes.append(Change(5, '5'))

        rb = RowBlock(changes)
        assert rb.size == 4
        assert rb[0] == '12345'
        assert rb[1] == '21354'
        assert rb[2] == '23145'
        assert rb[3] == '32415'

        rb = RowBlock(changes, '54321')
        assert rb[2] == '43521'

    def test_row_block_set_start(self):
        changes = []
        changes.append(Change(5, '3'))
        changes.append(Change(5, '1'))
        changes.append(Change(5, '5'))

        rb = RowBlock(changes)
        rb.set_start('54321')
        rb.recalculate()

        assert rb[2] == '43521'

    def test_row_block_recalculate(self):
        changes = []
        changes.append(Change(5, '3'))
        changes.append(Change(5, '1'))
        changes.append(Change(5, '5'))

        rb = RowBlock(changes)
        rb[2] = '54321'
        rb.recalculate(2)

        assert rb.size == 4
        assert rb[0] == '12345'
        assert rb[1] == '21354'
        assert rb[2] == '54321'
        assert rb[3] == '45231'

    def test_row_block_get_changes(self):
        changes = []
        rb = RowBlock(changes)

        assert rb.changes == changes
