Changelog
=========

.. currentmodule:: ringing

v0.5.0
------

* Updated Python version support:

   * ⚠️ **BREAKING CHANGE!** Dropped support for Python 3.8, 3.9, 3.10
   * Added support for Python 3.12, 3.13, 3.14, 3.15
   * Note that Python 3.11 is still supported

* Added new methods to :class:`Row`:

   *  :meth:`Row.conjugate()`
   *  :meth:`Row.num_cycles()`
   *  :meth:`Row.cycle_size()`

* ⚠️ **BREAKING CHANGE!** Renamed ``Group.symmetric_group`` and
   ``Group.alternating_group`` to match upstream.
   These are now :meth:`Group.symmetric` and :meth:`Group.alternating`
   respectively.

* Added new methods to :class:`Group`:

   *  :meth:`Group.trivial`
   *  :meth:`Group.dihedral_c`
   *  :meth:`Group.dihedral_r`
   *  :meth:`Group.cyclic_c`
   *  :meth:`Group.cyclic_r`
   *  :meth:`Group.direct_product`
   *  :meth:`Group.even_subgroup`

v0.4.0
------

*  Updated Python version support:

   *  ⚠️ **BREAKING CHANGE!** Dropped support for Python 2.6, 2.7, 3.3, 3.4
   *  Added support for Python 3.8, 3.9, 3.10, 3.11

v0.3.0
------

*  Reverted :class:`RowBlock` constructor invocation (introduced in ``v0.2.0``)

*  :class:`Bell` class

*  Modified the following methods to accept or return :class:`Bell`-shaped
   ducks:

   *  :meth:`Row.find`
   *  :meth:`Row.__getitem__`
   *  :meth:`Group.invariants`
   *  :meth:`Change.find_swap`
   *  :meth:`Change.find_place`
   *  :meth:`Change.swap_pair`
   *  :meth:`Change.__mul__`
   *  :meth:`Method.is_symmetric`
   *  :meth:`Method.is_palindromic`
   *  :meth:`Method.is_plain`
   *  :meth:`Method.has_dodges`
   *  :meth:`Method.has_places`
   *  :meth:`Method.symmetry_point`

v0.2.1
------

*  Bugfixes for the following hard crashes (segfaults):

   *  https://github.com/ringing-lib/ringing-lib-python/issues/5
   *  https://github.com/ringing-lib/ringing-lib-python/issues/6

v0.2.0
------

*  Modified constructor invocation for :class:`RowBlock` class

*  Improved documentation and exception error messages

*  Made sure to return ``NotImplemented`` as needed in operator implementations

*  :class:`Method` class

v0.1.0
------

First release.

*  Cython build system

*  Initial versions of the following classes:

   *  :class:`Row`
   *  :class:`Group`
   *  :class:`Change`
   *  :class:`RowBlock`
