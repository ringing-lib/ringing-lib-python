# cython: language_level=3

from libcpp cimport bool

from change cimport change


cdef extern from 'ringing/bell.h' namespace 'ringing':
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

        @staticmethod
        void set_symbols(char *syms)
