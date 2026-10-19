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

        # Workaround for two Cython issues:
        #  - we can't use ctypedef here
        #  - vector[T].const_iterator doesn't exist (use vector[T].iterator)
        cppclass const_iterator(vector[row].iterator):
            pass

        const_iterator begin()
        const_iterator end()
        size_t size()

        # Named constructors
        @staticmethod
        group symmetric(int nw, int nh, int nt)
        @staticmethod
        group alternating(int nw, int nh, int nt)

        @staticmethod
        group trivial(int nt)

        # These come in two version, _c and _r depending on whether the 
        # nw-cycle is row::cyclic or row::pblh.  D(n) is defined here 
        # as a group of order 2n.
        @staticmethod
        group dihedral_c(int nw, int nh, int nt);
        @staticmethod
        group dihedral_r(int nw, int nh, int nt);
        @staticmethod
        group cyclic_c(int nw, int nh, int nt);
        @staticmethod
        group cyclic_r(int nw, int nh, int nt);

        @staticmethod
        group direct_product(const group& a, const group& b);

        # Conjugate by r to get { r^-1 g r : g \in *this }
        group conjugate(const row& r)
        group even_subgroup()

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
