from cython.operator cimport dereference as deref
from cpython.version cimport PY_MAJOR_VERSION
from libcpp.string cimport string

from bell cimport bell


cdef string _s(s):
    if isinstance(s, unicode):
        return s.encode()
    else:
        return s


cdef class Row:

    cdef row *thisptr

    def __cinit__(self, input=None):
        if input is None:
            self.thisptr = new row()
        elif isinstance(input, Row):
            self.thisptr = new row(deref((<Row>input).thisptr))
        elif isinstance(input, int):
            self.thisptr = new row(<int>input)
        elif isinstance(input, str):
            self.thisptr = new row(_s(input))
        else:
            raise TypeError

    def __dealloc__(self):
        del self.thisptr

    def inverse(self):
        cdef Row result = Row()

        result.thisptr[0] = self.thisptr.inverse()
        return result

    @property
    def bells(self):
        return self.thisptr.bells()

    def rounds(self):
        self.thisptr.rounds()
        return self

    @staticmethod
    def rounds(int n):
        return Row(row.rounds(n))

    @staticmethod
    def queens(int n):
        return row.queens(n)

    @staticmethod
    def kings(int n):
        return row.kings(n)

    @staticmethod
    def tittums(int n):
        return row.tittums(n)

    @staticmethod
    def reverse_rounds(int n):
        return row.reverse_rounds(n)

    @staticmethod
    def cyclic(int n, int h=1, int c=1):
        return row.cyclic(n, h, c)

    @staticmethod
    def pblh(int n, int h=1):
        return row.pblh(n, h)

    def is_rounds(self):
        return self.thisptr.isrounds()

    def is_pblh(self, int hunts=0):
        if hunts:
            return self.thisptr.ispblh(hunts)
        else:
            return self.thisptr.ispblh()

    def sign(self):
        return self.thisptr.sign()

    def cycles(self):
        if PY_MAJOR_VERSION < 3:
            return self.thisptr.cycles()
        else:
            return self.thisptr.cycles().decode()

    def order(self):
        return self.thisptr.order()

    def __richcmp__(x, y, int op):
        cdef Row rx = Row(x)
        cdef Row ry = Row(y)

        if op == 0:  # <
            return deref(rx.thisptr) < deref(ry.thisptr)
        elif op == 1:  # <=
            return deref(rx.thisptr) <= deref(ry.thisptr)
        elif op == 2:  # ==
            return deref(rx.thisptr) == deref(ry.thisptr)
        elif op == 3:  # !=
            return deref(rx.thisptr) != deref(ry.thisptr)
        elif op == 4:  # >
            return deref(rx.thisptr) > deref(ry.thisptr)
        elif op == 5:  # >=
            return deref(rx.thisptr) >= deref(ry.thisptr)

    def __str__(self):
        return ''.join([
            chr(deref(self.thisptr)[i].to_char())
            for i
            in range(self.thisptr.bells())
        ])

    def __repr__(self):
        if self.thisptr.bells():
            return 'Row("' + self.__str__() + '")'
        else:
            return 'Row()'

    def __hash__(self):
        return self.thisptr.hash()

    def __mul__(x, y):
        cdef Row rx = Row(x)
        cdef Row ry = Row(y)
        cdef Row result = Row()

        result.thisptr[0] = deref(rx.thisptr) * deref(ry.thisptr)
        return result

    def __div__(x, y):
        return Row.__truediv__(x, y)

    def __truediv__(x, y):
        cdef Row rx = Row(x)
        cdef Row ry = Row(y)
        cdef Row result = Row()

        result.thisptr[0] = deref(rx.thisptr) / deref(ry.thisptr)
        return result

    def __pow__(Row x, int y, z):
        cdef Row rx = Row(x)
        cdef Row result = Row()

        result.thisptr[0] = rx.thisptr.power(y)
        return result

    def __invert__(self):
        return self.inverse()

    def __len__(self):
        return self.bells
