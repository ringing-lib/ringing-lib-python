cdef class Group:

    cdef group *thisptr

    cdef generator_list

    def __cinit__(self, *generators):
        cdef vector[row] generator_vector
        cdef Row current_row

        self.generator_list = []
        for generator in generators:
            current_row = Row(generator)
            generator_vector.push_back(deref(current_row.thisptr))
            self.generator_list.append(current_row)

        self.thisptr = new group(generator_vector)

    def __dealloc__(self):
        del self.thisptr

    property bells:
        def __get__(self):
            return self.thisptr.bells()

    property size:
        def __get__(self):
            return self.thisptr.size()

    def __richcmp__(x, y, int op):
        cdef group gx = deref((<Group?>x).thisptr)
        cdef group gy = deref((<Group?>y).thisptr)

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

    def __repr__(self):
        cdef str rows = ', '.join([repr(r) for r in self.generator_list])
        return 'Group({rows})'.format(rows=rows)

    def __iter__(self):
        return GroupIterator(self)

    def __len__(self):
        return self.size

cdef class GroupIterator:

    cdef group.const_iterator index

    cdef group.const_iterator end

    def __cinit__(self, Group g not None):
        self.index = deref(g.thisptr).begin()
        self.end = deref(g.thisptr).end()

    def __iter__(self):
        return self

    def __next__(self):
        cdef Row result = Row()

        if self.index == self.end:
            raise StopIteration

        result.thisptr[0] = deref(self.index)
        self.index += 1
        return result
