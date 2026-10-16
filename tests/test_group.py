import pytest

from ringing import Bell, Row, Group


class TestGroup:
    def test_group_constructor_exceptions(self):
        with pytest.raises(TypeError):
            Group(self)

    def test_group_bells(self):
        assert Group().bells == 0
        assert Group(6).bells == 6
        assert Group('13572468').bells == 8
        assert Group(6, 8).bells == 8

    def test_group_size(self):
        assert Group().size == 1
        assert Group(6).size == 1
        assert Group('134256').size == 3
        assert Group('213564', '123546').size == 12
        assert Group('654321').size == 2

    def test_group_named_groups(self):
        assert list(Group.symmetric_group(0)) == [Row()]
        assert list(Group.symmetric_group(3)) == ['123', '132', '213', '231', '312', '321']
        assert list(Group.symmetric_group(3, 1)) == ['1234', '1243', '1324', '1342', '1423', '1432']
        assert list(Group.symmetric_group(3, 1, 5)) == ['12345', '12435', '13245', '13425', '14235', '14325']

        assert list(Group.alternating_group(0)) == [Row()]
        assert list(Group.alternating_group(3)) == ['123', '231', '312']
        assert list(Group.alternating_group(3, 1)) == ['1234', '1342', '1423']
        assert list(Group.alternating_group(3, 1, 5)) == ['12345', '13425', '14235']

        with pytest.raises(ValueError):
            Group.symmetric_group(2, 2, 3)
        with pytest.raises(ValueError):
            Group.alternating_group(2, 2, 3)

    def test_group_conjugate(self):
        G = Group('2143', '1324')
        r = Row('1243')

        assert sorted([~r * g * r for g in G]) == sorted(G.conjugate(r))

    def test_group_coset_labels(self):
        G = Group('2143', '1324', '1243')  # S_4
        H = Group('2143', '1324')  # Rows in plain hunt

        # A row in G but not H; this must be in a coset of H.
        # This is the lexicographically lowest row (except rounds), so should be
        # the label of its coset.
        g = Row('1243')

        for h_dash in G:
            # gH is the left coset of H in G with respect to g
            lcoset_row = g * h_dash

            # Hg is the right coset of H in G with respect to g
            rcoset_row = h_dash * g

            if h_dash in H:
                assert H.lcoset_label(lcoset_row) == g
                assert H.rcoset_label(rcoset_row) == g
            else:
                assert H.lcoset_label(lcoset_row) != g
                assert H.rcoset_label(rcoset_row) != g

    def test_group_invariants(self):
        assert Group().invariants() == []
        assert Group(6).invariants() == list(range(6))
        assert Group('134256').invariants() == [0, 4, 5]
        assert Group('213564', '123546').invariants() == [2]
        assert Group('654321').invariants() == []

        assert type(Group('214536').invariants()[0]) == Bell

    def test_operators_return_not_implemented(self):
        # Arithmetic operator returns NotImplemented when given unknown types
        assert Group().__lt__(self) == NotImplemented
        assert Group().__le__(self) == NotImplemented
        assert Group().__eq__(self) == NotImplemented
        assert Group().__ne__(self) == NotImplemented
        assert Group().__gt__(self) == NotImplemented
        assert Group().__ge__(self) == NotImplemented

    def test_group_repr(self):
        tests = [
            'Group()',
            "Group(Row('134256'))",
            "Group(Row('213564'), Row('123546'))",
            'Group.symmetric_group(1, 2, 4)',
            'Group.alternating_group(1, 2, 4)',
        ]

        for test in tests:
            assert repr(eval(test)) == test

    def test_group_iterator(self):
        assert list(Group()) == [Row()]
        assert list(Group(6)) == ['123456']
        assert list(Group('134256')) == ['123456', '134256', '142356']
        assert list(Group('213564', '123546')) == [
            '123456', '123465', '123546', '123564', '123645', '123654',
            '213456', '213465', '213546', '213564', '213645', '213654',
        ]
        assert list(Group('654321')) == ['123456', '654321']

        # Check we can iterate over a group without holding a reference to it.
        # https://github.com/ringing-lib/ringing-lib-python/issues/5
        for r in Group.symmetric_group(2):
            pass
