# cython: language_level=3

from cython.operator cimport dereference as deref
from cpython.version cimport PY_MAJOR_VERSION
from libcpp.string cimport string

from bell cimport bell


cdef class Row:

    cdef row *thisptr

    def __cinit__(self, input=None):
        if input is None:
            self.thisptr = new row()
        elif isinstance(input, Row):
            self.thisptr = new row(deref((<Row>input).thisptr))
        elif isinstance(input, int):
            if 0 <= input <= 256:
                self.thisptr = new row(<int>input)
            else:
                raise ValueError('number of bells must be between 0 and 256')
        elif isinstance(input, unicode):
            self.thisptr = new row(<string>(input.encode()))
        elif isinstance(input, bytes):
            self.thisptr = new row(<string>input)
        else:
            raise TypeError

    def __dealloc__(self):
        del self.thisptr

    def inverse(self):
        cdef Row result = Row()
        result.thisptr[0] = self.thisptr.inverse()
        return result

    property bells:
        def __get__(self):
            return self.thisptr.bells()

    def make_rounds(self):
        self.thisptr.rounds()
        return self

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

    def __getitem__(self, int x):
        if 0 <= x <= (self.bells - 1):
            return <int>(deref(self.thisptr)[x])
        else:
            raise IndexError
