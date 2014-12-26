from cython.operator cimport dereference
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

    def __cinit__(self, input):
        if isinstance(input, int):
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
        return 'Row("' + self.__str__() + '")'

    def __str__(self):
        return ''.join([
            chr(dereference(self.thisptr)[i].to_char())
            for i
            in range(self.thisptr.bells())
        ])
