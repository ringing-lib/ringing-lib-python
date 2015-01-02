import unittest

from ringing import Row, Group


class GroupTest(unittest.TestCase):
    def test_group_constructor_exceptions(self):
        self.assertRaises(TypeError, lambda: Group(self))

    def test_group_bells(self):
        self.assertEqual(Group().bells, 0)
        self.assertEqual(Group(6).bells, 6)
        self.assertEqual(Group('13572468').bells, 8)
        self.assertEqual(Group(6, 8).bells, 8)

    def test_group_size(self):
        self.assertEqual(Group().size, 1)
        self.assertEqual(Group(6).size, 1)
        self.assertEqual(Group('134256').size, 3)
        self.assertEqual(Group('213564', '123546').size, 12)
        self.assertEqual(Group('654321').size, 2)

    def test_group_named_groups(self):
        self.assertEqual(list(Group.symmetric_group(0)), [Row()])
        self.assertEqual(
            list(Group.symmetric_group(3)),
            ['123', '132', '213', '231', '312', '321']
        )
        self.assertEqual(
            list(Group.symmetric_group(3, 1)),
            ['1234', '1243', '1324', '1342', '1423', '1432']
        )
        self.assertEqual(
            list(Group.symmetric_group(3, 1, 5)),
            ['12345', '12435', '13245', '13425', '14235', '14325']
        )

        self.assertEqual(list(Group.alternating_group(0)), [Row()])
        self.assertEqual(
            list(Group.alternating_group(3)),
            ['123', '231', '312']
        )
        self.assertEqual(
            list(Group.alternating_group(3, 1)),
            ['1234', '1342', '1423']
        )
        self.assertEqual(
            list(Group.alternating_group(3, 1, 5)),
            ['12345', '13425', '14235']
        )

        self.assertRaises(ValueError, lambda: Group.symmetric_group(2, 2, 3))
        self.assertRaises(ValueError, lambda: Group.alternating_group(2, 2, 3))

    def test_group_conjugate(self):
        G = Group('2143', '1324')
        r = Row('1243')

        self.assertEqual(
            sorted([~r * g * r for g in G]),
            sorted(G.conjugate(r))
        )

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
                self.assertEqual(H.lcoset_label(lcoset_row), g)
                self.assertEqual(H.rcoset_label(rcoset_row), g)
            else:
                self.assertNotEqual(H.lcoset_label(lcoset_row), g)
                self.assertNotEqual(H.rcoset_label(rcoset_row), g)

    def test_group_invariants(self):
        self.assertEqual(Group().invariants(), [])
        self.assertEqual(Group(6).invariants(), list(range(6)))
        self.assertEqual(Group('134256').invariants(), [0, 4, 5])
        self.assertEqual(Group('213564', '123546').invariants(), [2])
        self.assertEqual(Group('654321').invariants(), [])

    def test_group_repr(self):
        tests = [
            'Group()',
            "Group(Row('134256'))",
            "Group(Row('213564'), Row('123546'))",
            'Group.symmetric_group(1, 2, 4)',
            'Group.alternating_group(1, 2, 4)',
        ]

        for test in tests:
            self.assertEqual(repr(eval(test)), test)

    def test_group_iterator(self):
        self.assertEqual(list(Group()), [Row()])
        self.assertEqual(list(Group(6)), ['123456'])
        self.assertEqual(list(Group('134256')), ['123456', '134256', '142356'])
        self.assertEqual(list(Group('213564', '123546')), [
            '123456', '123465', '123546', '123564', '123645', '123654',
            '213456', '213465', '213546', '213564', '213645', '213654',
        ])
        self.assertEqual(list(Group('654321')), ['123456', '654321'])
