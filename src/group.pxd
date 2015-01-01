# cython: language_level=3

from libcpp cimport bool
from libcpp.vector cimport vector

from bell cimport bell
from row cimport row


cdef extern from 'ringing/group.h' namespace 'ringing':
    cdef cppclass group:
        group()  # The group containing just the identity
        group(const row& generator)
        group(const row& generator1, const row& generator2)
        group(const vector[row] &generators)

        size_t bells()

        # Container interface
        vector[row].iterator begin()
        vector[row].iterator end()
        size_t size()

        # Named constructors
        @staticmethod
        group symmetric_group(int nw)
        @staticmethod
        group symmetric_group(int nw, int nh)
        @staticmethod
        group symmetric_group(int nw, int nh, int nt)
        @staticmethod
        group alternating_group(int nw)
        @staticmethod
        group alternating_group(int nw, int nh)
        @staticmethod
        group alternating_group(int nw, int nh, int nt)

        # Conjugate by r to get { r^-1 g r : g \in *this }
        group conjugate(const row& r)

        bool operator==(const group& g)
        bool operator<(const group& g)
        bool operator>(const group& g)
        bool operator!=(const group& g)
        bool operator<=(const group& g)
        bool operator>=(const group& g)

        # Choose a element of the left coset rG or right coset Gr as a canonical
        # label for it.  The element chosen is the lexicographically least
        # element; thus if r \in G the label is rounds.  For part end groups,
        # you typically want right cosets.
        row rcoset_label(row& r)
        row lcoset_label(row& r)

        vector[bell] invariants()
