# cython: language_level=3

from libcpp cimport bool


cdef extern from "ringing/bell.h" namespace "ringing":
    cdef cppclass bell:
        bell()
        bell(int i) except +

        @staticmethod
        bell read_char(char c)

        char to_char()

        @staticmethod
        bool is_symbol(char c)
