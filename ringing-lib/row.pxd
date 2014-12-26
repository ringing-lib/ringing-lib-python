from libcpp cimport bool
from libcpp.string cimport string

from bell cimport bell


cdef extern from "ringing/row.h" namespace "ringing":
    cdef cppclass row:
        row(int) except +
        row(const string) except +
        bell operator[](int)
        int bells()
        bool isrounds()
        int order()
        int sign()
