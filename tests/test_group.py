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
    (Group.symmetric_group(0), [Row()]),
    (Group.symmetric_group(3), ['123', '132', '213', '231', '312', '321']),
    (Group.symmetric_group(3, 1), ['1234', '1243', '1324', '1342', '1423', '1432']),
    (Group.symmetric_group(3, 1, 5), ['12345', '12435', '13245', '13425', '14235', '14325']),
    (Group.alternating_group(0), [Row()]),
    (Group.alternating_group(3), ['123', '231', '312']),
    (Group.alternating_group(3, 1), ['1234', '1342', '1423']),
    (Group.alternating_group(3, 1, 5), ['12345', '13425', '14235']),
))
def test_named_groups(group, expected) -> None:
    assert list(group) == expected


def test_named_group_exceptions() -> None:
    with pytest.raises(ValueError):
        Group.symmetric_group(2, 2, 3)
    with pytest.raises(ValueError):
        Group.alternating_group(2, 2, 3)


def test_conjugate() -> None:
    G = Group('2143', '1324')
    r = Row('1243')

    assert sorted([~r * g * r for g in G]) == sorted(G.conjugate(r))


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
    'Group.symmetric_group(1, 2, 4)',
    'Group.alternating_group(1, 2, 4)',
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
    for _ in Group.symmetric_group(2):
        pass
