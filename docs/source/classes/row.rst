Rows
====

.. currentmodule:: ringing

For ease of notation, we use the idea that a row is an individual permutation of
bells (such as ``13572468``), and a change is a means of getting from one row to
another, by swapping pairs of bells; the most convenient way to write a change
is a place notation (for example ``X`` or ``1258``).

Row Operations
--------------

Rows have a set of operations which we can use on them; in mathematical terms,
they form a group. The most important operation is that of row multiplication or
transposition - in this operation, the bells in one row are rearranged according
to the order given by another row.

For example::

   21345678 × 13572468 = 23571468

and::

   13572468 × 21345678 = 31572468

Note that the two above examples do *not* give the same result; that is, the
order in which two things are multiplied does matter.

As an example of how row multiplication is used, suppose that we want to know
the 4th row of the lead of Plain Bob Major with lead head ``17856342``. The 4th
row of the first lead (which has a lead head of rounds) is ``42618375``.
Multiplying these together gives us the answer we are looking for, namely
``57312846``.

The identity for this operation is rounds; in other words, any row multiplied by
rounds gives itself, and rounds multiplied by any row gives that row.

It is possible to define the inverse of a row as the row which, when multiplied
by that row, will give rounds. For example, the inverse of ``13572468`` is
``15263748``, as::

   13572468 × 15263748 = 12345678

The opposite of row multiplication is row division. If ``a × b = c``, we can
define ``c / b = a``. Using the same example as above, suppose we have a lead of
Plain Bob Major and we know that the fourth row is ``57312846``, and we wish to
find the lead head. Just divide by the fourth row of the plain course
(``42618375``) to get the answer.

Row Properties
--------------

There are several properties of rows which arise from group theory and can be
useful in looking at properties of methods.

The *order* of a row is the number of times which that row has to be multiplied
by itself before it gets back to rounds. For example, the row ``21436587`` has
order 2, because if it is multiplied by itself twice, you get back to rounds.
Similarly the row ``23145678`` has order 3, and the row ``23456781`` has order
8. This can be useful, for example, in seeing how many leads of a method are
needed in a plain course before it comes round.

Another useful concept is the *sign* or *parity* of a row. A row is considered
*even* if it takes an even number of swaps of pairs of bells to get from rounds
to that row, and *odd* if it takes an odd number of swaps. (It can be shown that
whether the number is odd or even doesn't depend on exactly what the sequence of
swaps is).

Finally, every row can be expressed as a set of *cycles*. A cycle is a set of
bells which move round in a sequential way as the row is repeated; for example,
``21345678`` has only one cycle, which is ``(12)``; and ``12356478`` has one
cycle, which is ``(456)``. Combining these two cycles will give us the row
``213564678``.


The Row Class
-------------

.. autoclass:: Row(input: Row | int | str | bytes | None = None)

   .. method:: __lt__(row)
   .. method:: __le__(row)
   .. method:: __eq__(row)
   .. method:: __ne__(row)
   .. method:: __gt__(row)
   .. method:: __ge__(row)

      Compare a row to another::

         >>> from ringing import Row
         >>> Row(4) == '1234'
         True

      :param row: value to compare
      :type row: :class:`Row` or int or string
      :return: result
      :rtype: boolean

   .. automethod:: __getitem__(i: int)
   .. automethod:: __mul__(input: Change | Row | int | str | bytes) -> Row
   .. automethod:: __truediv__(Row | int | str | bytes) -> Row
   .. automethod:: __invert__
   .. automethod:: inverse
   .. automethod:: __pow__
   .. autoattribute:: bells
   .. automethod:: conjugate
   .. automethod:: rounds
   .. automethod:: queens
   .. automethod:: kings
   .. automethod:: tittums
   .. automethod:: reverse_rounds
   .. automethod:: pblh
   .. automethod:: cyclic
   .. automethod:: is_rounds
   .. automethod:: is_pblh
   .. automethod:: sign
   .. automethod:: cycles
   .. automethod:: num_cycles
   .. automethod:: cycle_size
   .. automethod:: order
   .. automethod:: find
   .. automethod:: conjugator
   .. automethod:: are_conjugate

The Group Class
---------------

.. autoclass:: Group(generator: Row[, generator: Row[, ...]])

   .. method:: __lt__(group)
   .. method:: __le__(group)
   .. method:: __eq__(group)
   .. method:: __ne__(group)
   .. method:: __gt__(group)
   .. method:: __ge__(group)

      Compare a group to another.

      :param group: value to compare
      :type group: :class:`Group`
      :return: result
      :rtype: boolean

   .. autoattribute:: bells
   .. autoattribute:: size
   .. automethod:: trivial
   .. automethod:: symmetric
   .. automethod:: alternating
   .. automethod:: dihedral_c
   .. automethod:: dihedral_r
   .. automethod:: cyclic_c
   .. automethod:: cyclic_r
   .. automethod:: direct_product
   .. automethod:: conjugate
   .. automethod:: even_subgroup
   .. automethod:: rcoset_label
   .. automethod:: lcoset_label
   .. automethod:: invariants
