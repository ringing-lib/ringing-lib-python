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

        char *name()                # Get name
        void name(const string& n)  # Set name
        string fullname()

        void push_back(const string &str)

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
        bool isplain()              # Does this bell plain hunt?
        bool isplain(bell b)
        bool hasdodges(bell b)      # Does this bell ever dodge?
        bool hasplaces(bell b)      # Does this bell make internal places?
        int methclass()             # What sort of method is it?
        char *lhcode()              # Return the lead head code
        int symmetry_point()        # Point of palindromic symmetry (or -1)
        int symmetry_point(bell b)  # Point of palindromic symmetry (or -1)
        int maxblows()              # Counts the maximum blows in one place

        bool is_palindromic_about(int i)
        bool is_palindromic_about(bell b, int i)

        string format()             # Format the place notation for output
        string format(int flags)
