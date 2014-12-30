# cython: language_level=3

from libcpp cimport bool
from libcpp.string cimport string


cdef extern from "ringing/change.h" namespace "ringing":
    cdef cppclass change:
        change()
        change(int num) except +
        change(int num, const string &s) except +
        change(const change& c)

        bool operator==(const change& c)
        bool operator!=(const change& c)

        string print()
        int bells()

        # So that we can put changes in containers
        bool operator<(const change& c)
        bool operator>(const change& c)
        bool operator<=(const change& c)
        bool operator>=(const change& c)
