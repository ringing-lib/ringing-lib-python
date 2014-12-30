# cython: language_level=3

from libcpp cimport bool
from libcpp.string cimport string

from bell cimport bell


cdef extern from "ringing/change.h" namespace "ringing":
    cdef cppclass change:
        change()
        change(int num) except +
        change(int num, const string &s) except +
        change(const change& c)  # Default copy constructor

        change& set(int num, const string &s)  # Assign from place notation
        bool operator==(const change& c)
        bool operator!=(const change& c)
        change reverse()                       # Return the reverse

        string print()           # Print place notation to a string
        int bells()              # Return number of bells
        int sign()               # Return whether it's odd or even
        bool findswap(bell b)    # Check whether a particular swap is done
        bool findplace(bell b)   # Check whether a particular place is made
        bool swappair(bell b) except +  # Swap or unswap a pair
        bool internal()          # Does it contain internal places?
        int count_places()       # Count the number of places made

        # So that we can put changes in containers
        bool operator<(const change& c)
        bool operator>(const change& c)
        bool operator<=(const change& c)
        bool operator>=(const change& c)
