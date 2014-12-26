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

    @property
    def bells(self):
        return self.thisptr.bells()

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

    def __repr__(self):
        if self.thisptr.bells():
            return 'Row("' + self.__str__() + '")'
        else:
            return 'Row()'

    def __str__(self):
        return ''.join([
            chr(deref(self.thisptr)[i].to_char())
            for i
            in range(self.thisptr.bells())
        ])

    def __hash__(self):
        return self.thisptr.hash()

    def __richcmp__(x, y, int op):
        if not isinstance(x, Row) or not isinstance(y, Row):
            raise NotImplementedError

        if op == 0:  # <
            return deref(Row(x).thisptr) < deref(Row(y).thisptr)
        elif op == 1:  # <=
            return deref(Row(x).thisptr) <= deref(Row(y).thisptr)
        elif op == 2:  # ==
            return deref(Row(x).thisptr) == deref(Row(y).thisptr)
        elif op == 3:  # !=
            return deref(Row(x).thisptr) != deref(Row(y).thisptr)
        elif op == 4:  # >
            return deref(Row(x).thisptr) > deref(Row(y).thisptr)
        elif op == 5:  # >=
            return deref(Row(x).thisptr) >= deref(Row(y).thisptr)

    def __mul__(x, y):
        cdef Row rx = Row(x)
        cdef Row ry = Row(y)
        cdef Row result = Row()

        result.thisptr[0] = deref(rx.thisptr) * deref(ry.thisptr)
        return result

    def __truediv__(x, y):
        cdef Row rx = Row(x)
        cdef Row ry = Row(y)
        cdef Row result = Row()

        result.thisptr[0] = deref(rx.thisptr) / deref(ry.thisptr)
        return result

    def __div__(x, y):
        return Row.__truediv__(x, y)
