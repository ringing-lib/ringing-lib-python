import functools

import pytest

from ringing import Bell, Row, Group


def test_constructor_exceptions() -> None:
    with pytest.raises(TypeError):
        Group([])


@pytest.mark.parametrize('input, expected', (
    ((None,), 0),
    ((6,), 6),
    (('13572468',), 8),
    ((6, 8), 8),
))
def test_bells(input, expected) -> None:
    assert Group(*input).bells == expected


@pytest.mark.parametrize('input, expected', (
    ((None,), 1),
    ((6,), 1),
    (('134256',), 3),
    (('213564', '123546'), 12),
    (('654321',), 2),
))
def test_size(input, expected) -> None:
    assert Group(*input).size == expected


@pytest.mark.parametrize('group, expected', (
    (Group.trivial(0), [Row()]),
    (Group.trivial(3), ['123']),
    (Group.symmetric(0), [Row()]),
    (Group.symmetric(3), ['123', '132', '213', '231', '312', '321']),
    (Group.symmetric(3, 1), ['1234', '1243', '1324', '1342', '1423', '1432']),
    (Group.symmetric(3, 1, 5), ['12345', '12435', '13245', '13425', '14235', '14325']),
    (Group.alternating(0), [Row()]),
    (Group.alternating(3), ['123', '231', '312']),
    (Group.alternating(3, 1), ['1234', '1342', '1423']),
    (Group.alternating(3, 1, 5), ['12345', '13425', '14235']),
    (Group.dihedral_c(0), [Row()]),
    (Group.dihedral_c(3), ['123', '132', '213', '231', '312', '321']),
    (Group.dihedral_c(4), ['1234', '1432', '2143', '2341', '3214', '3412', '4123', '4321']),
    (Group.dihedral_c(4, 1), ['12345', '12543', '13254', '13452', '14325', '14523', '15234', '15432']),
    (Group.dihedral_c(4, 1, 6), ['123456', '125436', '132546', '134526', '143256', '145236', '152346', '154326']),
    (Group.dihedral_r(0), [Row()]),
    (Group.dihedral_r(3), ['123', '132', '213', '231', '312', '321']),
    (Group.dihedral_r(4), ['1234', '2413', '3142', '4321']),
    (Group.dihedral_r(4, 1), ['12345', '13524', '14253', '15432']),
    (Group.dihedral_r(4, 1, 6), ['123456', '135246', '142536', '154326']),
    (Group.cyclic_c(0), [Row()]),
    (Group.cyclic_c(3), ['123', '231', '312']),
    (Group.cyclic_c(4), ['1234', '2341', '3412', '4123']),
    (Group.cyclic_c(4, 1), ['12345', '13452', '14523', '15234']),
    (Group.cyclic_r(0), [Row()]),
    (Group.cyclic_r(3), ['123', '231', '312']),
    (Group.cyclic_r(4), ['1234', '2413', '3142', '4321']),
    (Group.cyclic_r(5), ['12345', '24153', '31524', '45231', '53412']),
    (Group.cyclic_r(5, 1), ['123456', '135264', '142635', '156342', '164523']),
    (Group.cyclic_r(5, 1, 7), ['1234567', '1352647', '1426357', '1563427', '1645237']),
))
def test_named_groups(group: Group, expected: list[str]) -> None:
    assert list(group) == expected


@pytest.mark.parametrize('group, expected', (
    (Group.trivial(0), 1),
    (Group.trivial(10), 1),
    (Group.symmetric(0), 1),
    (Group.symmetric(1), 1),
    (Group.symmetric(2), 2),
    (Group.symmetric(3), 6),
    (Group.symmetric(4), 24),
    (Group.symmetric(5), 120),
    (Group.alternating(1), 1),
    (Group.alternating(2), 1),
    (Group.alternating(3), 3),
    (Group.alternating(4), 12),
    (Group.alternating(5), 60),
    (Group.dihedral_c(1), 1),
    (Group.dihedral_c(2), 2),
    (Group.dihedral_c(3), 6),
    (Group.dihedral_c(4), 8),
    (Group.dihedral_c(5), 10),
    (Group.dihedral_r(1), 1),
    (Group.dihedral_r(2), 2),
    (Group.dihedral_r(3), 6),
    (Group.dihedral_r(4), 4),  # reverse rounds is a pblh so only 4 here
    (Group.dihedral_r(5), 10),
    (Group.cyclic_c(1), 1),
    (Group.cyclic_c(2), 2),
    (Group.cyclic_c(3), 3),
    (Group.cyclic_c(4), 4),
    (Group.cyclic_c(5), 5),
    (Group.cyclic_c(7, 1), 7),  # 7-part cyclic major
    (Group.cyclic_c(11, 1), 11),  # 11-part cyclic maximus
    (Group.cyclic_c(12), 12),  # 11-part cyclic maximus
    (Group.cyclic_r(1), 1),
    (Group.cyclic_r(2), 2),
    (Group.cyclic_r(3), 3),
    (Group.cyclic_r(4), 4),
    (Group.cyclic_r(5), 5),
    (Group.cyclic_r(5, 1), 5),  # Plain Bob Minor
))
def test_group_orders(group: Group, expected: int) -> None:
    assert len(group) == expected


@pytest.mark.parametrize('group_name', (
    'symmetric',
    'alternating',
    'dihedral_c',
    'dihedral_r',
    'cyclic_c',
    'cyclic_r',
))
def test_too_few_working_bells(group_name: str) -> None:
    with pytest.raises(ValueError):
        getattr(Group, group_name)(2, 2, 3)


@pytest.mark.parametrize('groups, expected', (
    ((Group.trivial(0), Group.trivial(0)), Group.trivial(0)),
    ((Group.trivial(0), Group.trivial(1)), Group.trivial(1)),
    ((Group.trivial(1), Group.trivial(0)), Group.trivial(1)),
    ((Group.trivial(1), Group.trivial(1)), Group.trivial(2)),
    ((Group.trivial(4), Group('1324')), Group('12345768')),
    ((Group('2134'), Group('1324')), Group('12345768', '21345678')),
    ((Group.trivial(1), Group.cyclic_r(3)), Group.cyclic_r(3, 1)),  # Plain Bob Minimus lead heads
    ((Group.trivial(1), Group.cyclic_r(3), Group.trivial(2)), Group.cyclic_r(3, 1, 6)),
))
def test_direct_product(
    groups: tuple[Group],
    expected: Group,
) -> None:
    assert functools.reduce(Group.direct_product, groups) == expected


def test_conjugate() -> None:
    G = Group('2143', '1324')
    r = Row('1243')

    assert sorted([~r * g * r for g in G]) == sorted(G.conjugate(r))


@pytest.mark.parametrize('group, expected', (
    (Group('2134'), ['1234']),
    (Group.trivial(0), [Row()]),
    (Group.trivial(3), ['123']),
    (Group.symmetric(3), ['123', '231', '312']),
    (Group.alternating(3), ['123', '231', '312']),
))
def test_even_subgroup(group: Group, expected: list[str]) -> None:
    assert list(group.even_subgroup()) == expected


def test_coset_labels() -> None:
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


@pytest.mark.parametrize('input, expected', (
    ((), []),
    ((6,), list(range(6))),
    (('134256',), [0, 4, 5]),
    (('213564', '123546'), [2]),
    (('654321',), [])
))
def test_invariants(input, expected) -> None:
    assert Group(*input).invariants() == expected


def test_invariants_type() -> None:
    assert type(Group('214536').invariants()[0]) == Bell


OPERATORS = (
    '__lt__',
    '__le__',
    '__eq__',
    '__ne__',
    '__gt__',
    '__ge__',
)


@pytest.mark.parametrize('operator', OPERATORS)
def test_operators_return_not_implemented_for_unknown_types(operator) -> None:
    assert getattr(Group(), operator)([]) == NotImplemented


@pytest.mark.parametrize('input', (
    'Group()',
    "Group(Row('134256'))",
    "Group(Row('213564'), Row('123546'))",
    'Group.trivial(4)',
    'Group.symmetric(1, 2, 4)',
    'Group.alternating(1, 2, 4)',
    'Group.dihedral_c(1, 2, 4)',
    'Group.dihedral_r(1, 2, 4)',
    'Group.cyclic_c(1, 2, 4)',
    'Group.cyclic_r(1, 2, 4)',
    'Group.symmetric(1, 2, 4).even_subgroup()'
))
def test_repr(input: str) -> None:
    assert repr(eval(input)) == input


@pytest.mark.parametrize('group, expected', (
    (Group(), ['']),
    (Group(6), ['123456']),
    (Group('134256'), ['123456', '134256', '142356']),
    (Group('213564', '123546'), [
        '123456', '123465', '123546', '123564', '123645', '123654',
        '213456', '213465', '213546', '213564', '213645', '213654',
    ]),
    (Group('654321'), ['123456', '654321']),
))
def test_iterator(group: Group, expected: list[str]) -> None:
    assert list(group) == expected


def test_group_iteration() -> None:
    # Check we can iterate over a group without holding a reference to it.
    # https://github.com/ringing-lib/ringing-lib-python/issues/5
    for _ in Group.symmetric(2):
        pass
