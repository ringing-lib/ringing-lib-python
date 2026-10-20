# cython: language_level=3

from libcpp.vector cimport vector

from row cimport row
from change cimport change


cdef extern from 'ringing/row.h' namespace 'ringing':
    cdef cppclass row_block(vector[row]):
        row_block(const vector[change] &c)   # Starting from rounds
        row_block(const vector[change] &c, const row &r)

        const vector[change]& get_changes()  # Return the changes which we are
                                             # using

        row& set_start(const row& r)         # Set the first row
        row_block& recalculate(int start)    # Recalculate rows from changes
