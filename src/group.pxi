cdef class Group:

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

    property bells:
        def __get__(self) -> int:
            return self.thisptr.bells()

    property size:
        def __get__(self) -> int:
            return self.thisptr.size()

    @staticmethod
    def trivial(int total_bells) -> Group:
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
        cdef Group result = Group()
        result.thisptr[0] = group.direct_product(
            deref((<Group>a).thisptr),
            deref((<Group>b).thisptr),
        )
        return result

    def conjugate(self, r: RowSpec) -> Group:
        cdef Group result = Group()
        result.thisptr[0] = self.thisptr.conjugate(deref(Row(r).thisptr))
        return result

    def even_subgroup(self) -> Group:
        cdef Group result = Group()
        result.thisptr[0] = self.thisptr.even_subgroup()
        if self.repr_string:
            result.repr_string = f'{self.repr_string}.even_subgroup()'
        return result

    def rcoset_label(self, r: RowSpec) -> Row:
        cdef Row result = Row()
        result.thisptr[0] = self.thisptr.rcoset_label(deref(Row(r).thisptr))
        return result

    def lcoset_label(self, r: RowSpec) -> Row:
        cdef Row result = Row()
        result.thisptr[0] = self.thisptr.lcoset_label(deref(Row(r).thisptr))
        return result

    def invariants(self) -> list[Bell]:
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
