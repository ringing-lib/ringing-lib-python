from libcpp cimport bool
from libcpp.string cimport string


cdef extern from "ringing/row.h" namespace "ringing":
    cdef cppclass row:
        row(const string) except +
        int bells()
        bool isrounds()
        int order()
        int sign()
