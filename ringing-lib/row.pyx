from libcpp.string cimport string


cdef string _s(s):
    if type(s) is unicode:
        return s.encode()
    else:
        return s


cdef class Row:

    cdef row *thisptr

    def __cinit__(self, input):
        if type(input) is int:
            self.thisptr = new row(<int>input)
        elif type(input) is str:
            self.thisptr = new row(_s(input))
        else:
            raise TypeError

    def __dealloc__(self):
        del self.thisptr

    @property
    def bells(self):
        return self.thisptr.bells()

    @property
    def is_rounds(self):
        return self.thisptr.isrounds()

    @property
    def order(self):
        return self.thisptr.order()

    @property
    def sign(self):
        return self.thisptr.sign()
