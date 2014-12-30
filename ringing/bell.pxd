cdef extern from "ringing/bell.h" namespace "ringing":
    cdef cppclass bell:
        char to_char()
