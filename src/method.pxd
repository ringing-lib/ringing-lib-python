# cython: language_level=3

from libcpp cimport bool
from libcpp.string cimport string
from libcpp.vector cimport vector

from bell cimport bell
from change cimport change
from row cimport row


cdef extern from 'ringing/method.h' namespace 'ringing':
    cdef cppclass method(vector[change]):
        method()
        method(int l)
        method(int l, int b)
        method(int l, int b, const char *n)
        method(const string& pn, int b)  # Make a method from place notation
        method(const string& pn, int b, const string& n)
        method(const method& m)

        int length()
        int bells()
        row lh()
        bool issym()                # Is it palindromic about the usual point?
        bool ispalindromic()        # Is it palindromic about any point?
        bool isdouble()             # Is it double?
        bool isregular()            # Is it regular?
        int huntbells()             # Number of hunt bells
        int leads()                 # Number of leads in a plain course
        bool issym(bell b)          # Is this bell's path symmetrical?
        bool ispalindromic(bell b)  # Is it palindromic about any point?
        bool isplain(bell b=0)      # Does this bell plain hunt?
        bool hasdodges(bell b)      # Does this bell ever dodge?
        bool hasplaces(bell b)      # Does this bell make internal places?
        int methclass()             # What sort of method is it?
        char *lhcode()              # Return the lead head code
        int symmetry_point()        # Point of palindromic symmetry (or -1)
        int symmetry_point(bell b)  # Point of palindromic symmetry (or -1)
        int maxblows()              # Counts the maximum blows in one place
