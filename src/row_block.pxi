cdef class RowBlock:

    cdef row_block *thisptr

    cdef vector[change] change_vector

    cdef change_list

    def __cinit__(self, c, r=None):
        cdef row starting_row = deref(Row(r).thisptr)

        self.change_list = []
        for ch in c:
            if isinstance(ch, Change):
                self.change_vector.push_back(deref((<Change>ch).thisptr))
                self.change_list.append(ch)
            else:
                raise TypeError('change list contained invalid type')

        if r is None:
            self.thisptr = new row_block(self.change_vector)
        else:
            self.thisptr = new row_block(self.change_vector, starting_row)

    def __dealloc__(self):
        del self.thisptr

    property size:
        def __get__(self):
            return self.thisptr.size()

    property changes:
        def __get__(self):
            return self.change_list

    def set_start(self, r):
        cdef Row rr = Row(r)
        self.thisptr.set_start(deref(rr.thisptr))
        return rr

    def recalculate(self, int start=0):
        if 0 <= start < self.size:
            self.thisptr.recalculate(start)
            return self
        else:
            raise IndexError

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
