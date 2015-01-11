# cython: language_level=3

from cython.operator cimport dereference as deref
from cpython.version cimport PY_MAJOR_VERSION
from libcpp.string cimport string
from libcpp.vector cimport vector

from bell cimport *
from change cimport *
from group cimport *
from method cimport *
from row cimport *
from row_block cimport *

MAX_BELLS = bell().MAX_BELLS

cdef int MAX_BELL_NUMBER = 255

include 'row.pxi'
include 'group.pxi'
include 'change.pxi'
include 'row_block.pxi'
include 'method.pxi'
