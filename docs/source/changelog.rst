Changelog
=========

.. currentmodule:: ringing

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
