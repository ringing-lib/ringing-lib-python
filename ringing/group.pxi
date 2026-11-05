cdef class Group:
    """
    Generates a group of rows.

    Once created, groups can be tested for membership or iterated over using
    the ``in`` operator (and hence converted to lists via ``list()``).
    Groups are immutable.

    :param generator: generators for the group (rows)
    :type generator: :class:`Row` or int or string
    """

    cdef group *thisptr

    cdef generator_list

    cdef repr_string

    def __cinit__(self, *generators: Row):
        cdef vector[row] generator_vector
        cdef Row current_row

        self.generator_list = []
        self.repr_string = None

        for generator in generators:
            current_row = Row(generator)
            generator_vector.push_back(deref(current_row.thisptr))
            self.generator_list.append(current_row)

        self.thisptr = new group(generator_vector)

    def __dealloc__(self):
        del self.thisptr

    @property
    def bells(self) -> int:
        """
        Number of bells which the group's rows contain:

        >>> from ringing import Group
        >>> Group('2143', '1324').bells
        4

        """
        return self.thisptr.bells()

    @property
    def size(self) -> int:
        """
        Number of rows which the group contains (the *order* of the group):

        >>> from ringing import Group
        >>> Group('2143', '1324').size  # generators for plain hunt
        8

        You may prefer to use the ``len()`` of the group.
        """
        return self.thisptr.size()

    @staticmethod
    def trivial(int total_bells) -> Group:
        """
        Returns the trivial group of order 1:

        >>> from ringing import Group
        >>> list(Group.trivial(4))
        [Row('1234')]

        :param int total_bells: number of bells in each row
        :return: the computed group
        :rtype: :class:`Group`
        """
        cdef Group result = Group()
        result.repr_string = f'Group.trivial({total_bells})'
        result.thisptr[0] = group.trivial(total_bells)
        return result

    @staticmethod
    def symmetric(
        int working_bells,
        int hunt_bells = 0,
        int total_bells = 0,
    ) -> Group:
        """
        Returns the symmetric group S\ :sub:`n` containing all permutations on
        *n* bells, i.e. the extent:

        >>> from ringing import Group
        >>> list(Group.symmetric(3))
        [Row('123'), Row('132'), Row('213'), Row('231'), Row('312'), Row('321')]

        By specifying *hunt_bells* and *total_bells* it's possible to produce
        groups with more fixed bells, e.g.:

        >>> from ringing import Group
        >>> list(Group.symmetric(3, 1, 6))
        [Row('123456'), Row('124356'), Row('132456'), Row('134256'), Row('142356'), Row('143256')]

        :param int working_bells: *n*, number of bells involved in permutations
        :param int hunt_bells: number of fixed bells at the start of the change
        :param int total_bells: number of bells in each row
        :return: the computed group
        :rtype: :class:`Group`
        :raises: :exc:`ValueError` if *total_bells* is less than the sum of
            *working_bells* and *hunt_bells*
        """
        if total_bells and total_bells < working_bells + hunt_bells:
            raise ValueError(
                'total_bells must be greater than working_bells + hunt_bells',
            )

        cdef Group result = Group()
        result.repr_string = \
            f'Group.symmetric({working_bells}, {hunt_bells}, {total_bells})'
        result.thisptr[0] = group.symmetric(
            working_bells,
            hunt_bells,
            total_bells,
        )
        return result

    @staticmethod
    def alternating(
        int working_bells,
        int hunt_bells = 0,
        int total_bells = 0,
    ) -> Group:
        """
        Returns the alternating group A\ :sub:`n` containing all even
        permutations on *n* bells (see :meth:`Row.sign`):

        >>> from ringing import Group
        >>> list(Group.alternating(3))
        [Row('123'), Row('231'), Row('312')]

        :param int working_bells: *n*, number of bells involved in permutations
        :param int hunt_bells: number of fixed bells at the start of the change
        :param int total_bells: number of bells in each row
        :return: the computed group
        :rtype: :class:`Group`
        :raises: :exc:`ValueError` if *total_bells* is less than the sum of
            *working_bells* and *hunt_bells*
        """
        if total_bells and total_bells < working_bells + hunt_bells:
            raise ValueError(
                'total_bells must be greater than working_bells + hunt_bells',
            )

        cdef Group result = Group()
        result.repr_string = \
            f'Group.alternating({working_bells}, {hunt_bells}, {total_bells})'
        result.thisptr[0] = group.alternating(
            working_bells,
            hunt_bells,
            total_bells,
        )
        return result

    @staticmethod
    def dihedral_c(
        int working_bells,
        int hunt_bells = 0,
        int total_bells = 0,
    ) -> Group:
        """
        Returns the dihedral group D\ :sub:`n` containing the symmetries of a
        regular *n*-gon, i.e. rotations and reflections.
        The ``_c`` variant uses cyclic lead heads.
        Its generators are the first cyclic lead head and reverse rounds.

        >>> from ringing import Group
        >>> list(Group.dihedral_c(4))
        [Row('1234'), Row('1432'), Row('2143'), Row('2341'), Row('3214'), Row('3412'), Row('4123'), Row('4321')]

        :param int working_bells: *n*, number of bells involved in permutations
        :param int hunt_bells: number of fixed bells at the start of the change
        :param int total_bells: number of bells in each row
        :return: the computed group
        :rtype: :class:`Group`
        :raises: :exc:`ValueError` if *total_bells* is less than the sum of
            *working_bells* and *hunt_bells*
        """
        if total_bells and total_bells < working_bells + hunt_bells:
            raise ValueError(
                'total_bells must be greater than working_bells + hunt_bells',
            )

        cdef Group result = Group()
        result.repr_string = \
            f'Group.dihedral_c({working_bells}, {hunt_bells}, {total_bells})'
        result.thisptr[0] = group.dihedral_c(
            working_bells,
            hunt_bells,
            total_bells,
        )
        return result

    @staticmethod
    def dihedral_r(
        int working_bells,
        int hunt_bells = 0,
        int total_bells = 0,
    ) -> Group:
        """
        Returns the dihedral group D\ :sub:`n` containing the symmetries of a
        regular *n*-gon, i.e. rotations and reflections.
        The ``_r`` variant uses plain bob lead heads.
        Its generators are the first plain bob lead head and reverse rounds.

        >>> from ringing import Group
        >>> list(Group.dihedral_r(4))
        [Row('1234'), Row('2413'), Row('3142'), Row('4321')]

        :param int working_bells: *n*, number of bells involved in permutations
        :param int hunt_bells: number of fixed bells at the start of the change
        :param int total_bells: number of bells in each row
        :return: the computed group
        :rtype: :class:`Group`
        :raises: :exc:`ValueError` if *total_bells* is less than the sum of
            *working_bells* and *hunt_bells*
        """
        if total_bells and total_bells < working_bells + hunt_bells:
            raise ValueError(
                'total_bells must be greater than working_bells + hunt_bells',
            )

        cdef Group result = Group()
        result.repr_string = \
            f'Group.dihedral_r({working_bells}, {hunt_bells}, {total_bells})'
        result.thisptr[0] = group.dihedral_r(
            working_bells,
            hunt_bells,
            total_bells,
        )
        return result

    @staticmethod
    def cyclic_c(
        int working_bells,
        int hunt_bells = 0,
        int total_bells = 0,
    ) -> Group:
        """
        Returns the cyclic group C\ :sub:`n` containing the rotations of a
        regular *n*-gon.
        The ``_c`` variant uses cyclic lead heads.
        Its generator is the first cyclic lead head.

        >>> from ringing import Group
        >>> list(Group.cyclic_c(4))
        [Row('1234'), Row('2341'), Row('3412'), Row('4123')]

        :param int working_bells: *n*, number of bells involved in permutations
        :param int hunt_bells: number of fixed bells at the start of the change
        :param int total_bells: number of bells in each row
        :return: the computed group
        :rtype: :class:`Group`
        :raises: :exc:`ValueError` if *total_bells* is less than the sum of
            *working_bells* and *hunt_bells*
        """
        if total_bells and total_bells < working_bells + hunt_bells:
            raise ValueError(
                'total_bells must be greater than working_bells + hunt_bells',
            )

        cdef Group result = Group()
        result.repr_string = \
            f'Group.cyclic_c({working_bells}, {hunt_bells}, {total_bells})'
        result.thisptr[0] = group.cyclic_c(
            working_bells,
            hunt_bells,
            total_bells,
        )
        return result

    @staticmethod
    def cyclic_r(
        int working_bells,
        int hunt_bells = 0,
        int total_bells = 0,
    ) -> Group:
        """
        Returns the cyclic group C\ :sub:`n` containing the rotations of a
        regular *n*-gon.
        The ``_r`` variant uses plain bob lead heads.
        Its generator is the first plain bob lead head.

        >>> from ringing import Group
        >>> list(Group.cyclic_r(4))
        [Row('1234'), Row('2413'), Row('3142'), Row('4321')]

        :param int working_bells: *n*, number of bells involved in permutations
        :param int hunt_bells: number of fixed bells at the start of the change
        :param int total_bells: number of bells in each row
        :return: the computed group
        :rtype: :class:`Group`
        :raises: :exc:`ValueError` if *total_bells* is less than the sum of
            *working_bells* and *hunt_bells*
        """
        if total_bells and total_bells < working_bells + hunt_bells:
            raise ValueError(
                'total_bells must be greater than working_bells + hunt_bells',
            )

        cdef Group result = Group()
        result.repr_string = \
            f'Group.cyclic_r({working_bells}, {hunt_bells}, {total_bells})'
        result.thisptr[0] = group.cyclic_r(
            working_bells,
            hunt_bells,
            total_bells,
        )
        return result

    @staticmethod
    def direct_product(Group a, Group b) -> Group:
        """
        Combines two groups by computing their direct product.
        Bells of group ``b`` are shifted right to make room for the bells in
        group ``a`` and then the cartesian product is computed:

        >>> from ringing import Group
        >>> a = Group('2134')  # ['1234', '2134']
        >>> b = Group('1324')  # ['1234', '1324']
        >>> list(Group.direct_product(a, b))
        [Row('12345678'), Row('12345768'), Row('21345678'), Row('21345768')]

        :param a: first group
        :type a: :class:`Group`
        :param b: second group
        :type b: :class:`Group`
        :return: the computed group
        :rtype: :class:`Group`
        """
        cdef Group result = Group()
        result.thisptr[0] = group.direct_product(
            deref((<Group>a).thisptr),
            deref((<Group>b).thisptr),
        )
        return result

    def conjugate(self, r: RowSpec) -> Group:
        """
        Conjugates the group by a row *r*, in pseudocode::

            H = (r ^ -1) . g . r for g in G

        :param r: row *r*
        :type r: :class:`Row` or int or string
        :return: the computed group
        :rtype: :class:`Group`
        """
        cdef Group result = Group()
        result.thisptr[0] = self.thisptr.conjugate(deref(Row(r).thisptr))
        return result

    def even_subgroup(self) -> Group:
        """
        Returns the subgroup where all rows are even (see :meth:`Row.sign`):

        >>> from ringing import Group
        >>> Group.symmetric(4).even_subgroup() == Group.alternating(4)
        True

        :return: the computed group
        :rtype: :class:`Group`
        """
        cdef Group result = Group()
        result.thisptr[0] = self.thisptr.even_subgroup()
        if self.repr_string:
            result.repr_string = f'{self.repr_string}.even_subgroup()'
        return result

    def rcoset_label(self, r: RowSpec) -> Row:
        """
        Returns the label of the right coset of G in S\ :sub:`n` with respect
        to the row *r*.

        A subgroup H of S\ :sub:`n` partitions the group into ``n! / |G|``
        cosets.

        * *g*\ H is the left coset of H in G with respect to *g*
        * H\ *g* is the right coset of H in G with respect to *g*

        Each coset may be conveniently labelled by choosing the
        lexicographically least element within it.

        :param r: row *r*
        :type r: :class:`Row` or int or string
        :return: the computed label
        :rtype: :class:`Row`
        """
        cdef Row result = Row()
        result.thisptr[0] = self.thisptr.rcoset_label(deref(Row(r).thisptr))
        return result

    def lcoset_label(self, r: RowSpec) -> Row:
        """
        Returns the label of the left coset of G in S\ :sub:`n` with respect
        to the row *r*.

        A subgroup H of S\ :sub:`n` partitions the group into ``n! / |G|``
        cosets.

        * *g*\ H is the left coset of H in G with respect to *g*
        * H\ *g* is the right coset of H in G with respect to *g*

        Each coset may be conveniently labelled by choosing the
        lexicographically least element within it.

        :param r: row *r*
        :type r: :class:`Row` or int or string
        :return: the computed label
        :rtype: :class:`Row`
        """
        cdef Row result = Row()
        result.thisptr[0] = self.thisptr.lcoset_label(deref(Row(r).thisptr))
        return result

    def invariants(self) -> list[Bell]:
        """
        Returns a list of invariant bells as 0-indexed integers, e.g.:

        >>> from ringing import Group
        >>> Group.alternating(3, 1, 8).invariants()
        [Bell(0), Bell(4), Bell(5), Bell(6), Bell(7)]

        :return: invariant bells
        :rtype: [:class:`Bell`]
        """
        cdef vector[bell] invariants = self.thisptr.invariants()
        return [Bell(<int>invariant) for invariant in invariants]

    def __richcmp__(self, other, int op) -> bool:
        cdef group gx
        cdef group gy

        if not isinstance(other, Group):
            return NotImplemented

        gx = deref((<Group>self).thisptr)
        gy = deref((<Group>other).thisptr)

        if op == 0:  # <
            return gx < gy
        elif op == 1:  # <=
            return gx <= gy
        elif op == 2:  # ==
            return gx == gy
        elif op == 3:  # !=
            return gx != gy
        elif op == 4:  # >
            return gx > gy
        elif op == 5:  # >=
            return gx >= gy

    def __repr__(self) -> str:
        if self.repr_string:
            return self.repr_string
        else:
            return 'Group({rows})'.format(
                rows=', '.join([repr(r) for r in self.generator_list]),
            )

    def __iter__(self) -> GroupIterator:
        return GroupIterator(self)

    def __len__(self) -> int:
        return self.size


cdef class GroupIterator:

    cdef Group g

    cdef group.const_iterator index

    cdef group.const_iterator end

    def __cinit__(self, Group g not None):
        self.g = g
        self.index = deref(g.thisptr).begin()
        self.end = deref(g.thisptr).end()

    def __iter__(self) -> GroupIterator:
        return self

    def __next__(self) -> Row:
        cdef Row result = Row()

        if self.index == self.end:
            raise StopIteration

        result.thisptr[0] = deref(self.index)
        self.index += 1
        return result
