cdef class Row:

    cdef row *thisptr

    def __cinit__(self, input=None):
        if input is None:
            self.thisptr = new row()
        elif isinstance(input, Row):
            self.thisptr = new row(deref((<Row>input).thisptr))
        elif isinstance(input, int):
            if 0 <= input <= MAX_BELL_NUMBER:
                self.thisptr = new row(<int>input)
            else:
                raise ValueError('Number of bells out of range')
        elif isinstance(input, unicode):
            self.thisptr = new row(<string>(input.encode()))
        elif isinstance(input, bytes):
            self.thisptr = new row(<string>input)
        else:
            raise TypeError('Cannot convert {type} to ringing.Row'.format(
                type=type(input).__name__
            ))

    def __dealloc__(self):
        del self.thisptr

    def inverse(self):
        cdef Row result = Row()
        result.thisptr[0] = self.thisptr.inverse()
        return result

    property bells:
        def __get__(self):
            return self.thisptr.bells()

    @staticmethod
    def rounds(int n):
        cdef Row result = Row()
        result.thisptr[0] = row.rounds(n)
        return result

    @staticmethod
    def queens(int n):
        cdef Row result = Row()
        result.thisptr[0] = row.queens(n)
        return result

    @staticmethod
    def kings(int n):
        cdef Row result = Row()
        result.thisptr[0] = row.kings(n)
        return result

    @staticmethod
    def tittums(int n):
        cdef Row result = Row()
        result.thisptr[0] = row.tittums(n)
        return result

    @staticmethod
    def reverse_rounds(int n):
        cdef Row result = Row()
        result.thisptr[0] = row.reverse_rounds(n)
        return result

    @staticmethod
    def cyclic(int n, int h=1, int c=1):
        cdef Row result = Row()
        result.thisptr[0] = row.cyclic(n, h, c)
        return result

    @staticmethod
    def pblh(int n, int h=1):
        cdef Row result = Row()
        result.thisptr[0] = row.pblh(n, h)
        return result

    def is_rounds(self):
        return self.thisptr.isrounds()

    def is_pblh(self, int hunts=0):
        if hunts:
            result = self.thisptr.ispblh(hunts)
        else:
            result = self.thisptr.ispblh()

        if result == 0:
            result = False

        return result

    def sign(self):
        return self.thisptr.sign()

    def cycles(self):
        if PY_MAJOR_VERSION < 3:
            return self.thisptr.cycles()
        else:
            return self.thisptr.cycles().decode()

    def order(self):
        return self.thisptr.order()

    def find(self, b):
        cdef bell bb = deref(Bell(b).thisptr)
        return self.thisptr.find(bb)

    @staticmethod
    def conjugator(x, y):
        cdef Row result = Row()
        result.thisptr[0] = conjugator(deref(Row(x).thisptr),
                                       deref(Row(y).thisptr))
        if result == Row():
            return None
        else:
            return result

    @staticmethod
    def are_conjugate(x, y):
        return are_conjugate(deref(Row(x).thisptr), deref(Row(y).thisptr))

    def __richcmp__(x, y, int op):
        cdef row rx
        cdef row ry

        try:
            rx = deref(Row(x).thisptr)
            ry = deref(Row(y).thisptr)
        except TypeError:
            return NotImplemented

        if op == 0:  # <
            return rx < ry
        elif op == 1:  # <=
            return rx <= ry
        elif op == 2:  # ==
            return rx == ry
        elif op == 3:  # !=
            return rx != ry
        elif op == 4:  # >
            return rx > ry
        elif op == 5:  # >=
            return rx >= ry

    def __str__(self):
        if PY_MAJOR_VERSION < 3:
            return self.__bytes__()
        else:
            return self.__unicode__()

    def __bytes__(self):
        return self.thisptr.print()

    def __unicode__(self):
        return self.thisptr.print().decode()

    def __repr__(self):
        if self.thisptr.bells():
            return "Row('" + self.__str__() + "')"
        else:
            return 'Row()'

    def __hash__(self):
        return self.thisptr.hash()

    def __mul__(x, y):
        cdef Row result = Row()

        try:
            if isinstance(y, Change):
                result.thisptr[0] = deref(Row(x).thisptr) * \
                                    deref((<Change>y).thisptr)
            else:
                result.thisptr[0] = deref(Row(x).thisptr) * \
                                    deref(Row(y).thisptr)
        except TypeError:
            return NotImplemented
        else:
            return result

    def __div__(x, y):
        return Row.__truediv__(x, y)

    def __truediv__(x, y):
        cdef Row result = Row()

        try:
            result.thisptr[0] = deref(Row(x).thisptr) / deref(Row(y).thisptr)
        except TypeError:
            return NotImplemented
        else:
            return result

    def __pow__(Row x, int y, z):
        cdef Row result = Row()
        result.thisptr[0] = Row(x).thisptr.power(y)
        return result

    def __invert__(self):
        return self.inverse()

    def __len__(self):
        return self.bells

    def __getitem__(self, int x):
        if 0 <= x < self.bells:
            return Bell(<int>(deref(self.thisptr)[x]))
        else:
            raise IndexError('ringing.Row index out of range')
