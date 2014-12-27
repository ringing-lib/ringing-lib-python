# cython: language_level=3

from libcpp cimport bool
from libcpp.string cimport string

from bell cimport bell


cdef extern from "ringing/row.h" namespace "ringing":
    cdef cppclass row:
        row()
        row(int num) except +               # Construct rounds on n bells
        row(const string &s) except +       # Construct a row from a string
        row(const row& r)                   # Default copy constructor

        bool operator==(const row& r)       # Compare
        bool operator!=(const row& r)
        bell operator[](int i)              # Return one particular bell
        row operator*(const row& r)         # Transpose one row by another
        row operator/(const row& r)         # Inverse of transposition
        row inverse()                       # Find the inverse
        row power(int n)                    # Find the nth power of the row

        string print()                      # Print the row into a string
        int bells()                         # How many bells?
        row &rounds()                       # Set it to rounds

        @staticmethod
        row rounds(int n)                   # Return rounds on n bells
        @staticmethod
        row queens(int n)                   # Return queens on n bells
        @staticmethod
        row kings(int n)                    # Return kings on n bells
        @staticmethod
        row tittums(int n)                  # Return tittums on n bells
        @staticmethod
        row reverse_rounds(int n)           # Return reverse rounds on n bells
        @staticmethod
        row cyclic(int n)                   # Return cyclic lead head
        @staticmethod                       # (13456..2)^c on n bells with h
        row cyclic(int n, int h)            # hunt bells
        @staticmethod
        row cyclic(int n, int h, int c)
        @staticmethod
        row pblh(int n)                     # Return first plain bob lead head
        @staticmethod                       # on n bells with h hunt bells
        row pblh(int n, int h)

        bool isrounds()     # Is it rounds?
        int ispblh()        # Which plain bob lead head is it?
        int ispblh(int h)   # Which plain bob lh (with h hunts) is it?
        int sign()          # Return whether it's odd or even
        string cycles()     # Express it as a product of disjoint cycles
        int order()         # Return the order
        size_t hash()

        # So that we can put rows in containers
        bool operator<(const row& r)
        bool operator>(const row& r)
        bool operator<=(const row& r)
        bool operator>=(const row& r)
