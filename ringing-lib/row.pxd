from libcpp cimport bool
from libcpp.string cimport string

from bell cimport bell


cdef extern from "ringing/row.h" namespace "ringing":
    cdef cppclass row:
        row(int num) except +               # Construct rounds on n bells
        row(const string &s) except +       # Construct a row from a string

        bell operator[](int i)              # Return one particular bell

        int bells()                         # How many bells?

        bool isrounds()                     # Is it rounds?
        int sign()                          # Return whether it's odd or even
        int order()                         # Return the order
