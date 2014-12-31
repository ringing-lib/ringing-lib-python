cdef class RowBlock:

    cdef row_block *thisptr

    def __cinit__(self, c, r=None):
        cdef vector[change] changes
        cdef row starting_row = deref(Row(r).thisptr)

        for ch in c:
            if isinstance(ch, Change):
                changes.push_back(deref((<Change>ch).thisptr))
            else:
                raise TypeError('change list contained invalid type')

        if r is None:
            self.thisptr = new row_block(changes)
        else:
            self.thisptr = new row_block(changes, starting_row)

    def __dealloc__(self):
        del self.thisptr

    property size:
        def __get__(self):
            return self.thisptr.size()

    def set_start(self, r):
        cdef Row rr = Row(r)
        self.thisptr.set_start(deref(rr.thisptr))
        return rr

    def recalculate(self, int start=0):
        self.thisptr.recalculate(start)
        return self

    def __len__(self):
        return self.size

    def __getitem__(self, int x):
        cdef Row result = Row()

        if 0 <= x < self.size:
            result.thisptr[0] = deref(self.thisptr)[x]
            return result
        else:
            raise IndexError

    def __setitem__(self, int x, y):
        cdef Row ry = Row(y)

        if 0 <= x < self.size:
            deref(self.thisptr)[x] = deref(ry.thisptr)
        else:
            raise IndexError
