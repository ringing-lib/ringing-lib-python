from libcpp.string cimport string

cimport row


cdef class Row:

    cdef row *thisptr

    def __cinit__(self, const string str):
        self.thisptr = new row(str)

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
