# cython: language_level=3

from libcpp cimport bool

from change cimport change


cdef extern from "ringing/bell.h" namespace "ringing":
    cdef cppclass bell:
        @staticmethod
        unsigned int MAX_BELLS

        bell()
        bell(int i) except +

        @staticmethod
        bell read_char(char c)

        char to_char()

        @staticmethod
        bool is_symbol(char c)

        # WARNING: this is actually defined in change.h.
        # Cython doesn't seem to support operators not attached to a class.
        bell operator*(const change& c)  # Apply a change to a position
