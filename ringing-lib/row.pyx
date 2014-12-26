from libcpp.string cimport string

cimport row


cdef bytes _s(s):
    if type(s) is unicode:
        return s.encode()
    else:
        return s


cdef class Row:

    cdef row *thisptr

    def __cinit__(self, str input):
        self.thisptr = new row(_s(input))

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
