Rows
====

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

.. currentmodule:: ringing

.. class:: Row([spec])
   
   Constructs a Row.
   
   :param spec: Specification for constructing the row.
      This might be:
      
      *  Nothing. Constructs a row on zero bells.
      *  Another row. Constructs a copy.
      *  An integer number of bells. Constructs rounds.
      *  A string (unicode or bytes) representation of a row.
   :type spec: :class:`Row` or integer or string
   :raises: :exc:`ValueError` if ``spec`` can't be parsed
   :raises: :exc:`TypeError` if ``spec`` is of an unknown type
   
   .. method:: __lt__(row)
   .. method:: __le__(row)
   .. method:: __eq__(row)
   .. method:: __ne__(row)
   .. method:: __gt__(row)
   .. method:: __ge__(row)
      
      Compare a row to another.
      
      :param row: value to compare
      :type row: :class:`Row` or integer or string
      :return: result
      :rtype: boolean
      :raises: :exc:`ValueError` if ``row`` can't be parsed
      :raises: :exc:`TypeError` if ``row`` is of an unknown type
   
   .. method:: __getitem__(i)
      
      This returns the *i*\ th bell in the row. Note that this is not an lvalue,
      so you cannot assign a value to an individual bell in a row.
      
      :param int i: bell position to return (0-indexed)
      :return: bell number in that position (0-indexed; ``0`` is the treble)
      :rtype: int
   
   .. method:: __mul__(row)
      
      Multiplies two rows together as explained above. If the rows are not of
      the same length, the shorter row is considered to be first padded out to
      the length of the longer row by adding the extra bells in order at the
      end.
      
      :param row: value to multiply by
      :type row: :class:`Row` or integer or string
      :return: result
      :rtype: :class:`Row`
      :raises: :exc:`ValueError` if ``row`` can't be parsed
      :raises: :exc:`TypeError` if ``row`` is of an unknown type
   
   .. method:: __mul__(change)
      
      Applies a change to a row. If the number of bells *c* differs from the
      number of bells in *r*\ , then *c* is considered to be padded or truncated
      in the obvious way.
      
      :param change: change to apply
      :type change: :class:`Change`
      :return: result
      :rtype: :class:`Row`
   
   .. method:: __div__(row)
      
      Divides two rows, as explained above. If the rows are not of the same
      length, the shorter row is considered to be first padded out to the length
      of the longer row by adding the extra bells in order at the end.
      
      :param row: value to divide by
      :type row: :class:`Row` or integer or string
      :return: result
      :rtype: :class:`Row`
      :raises: :exc:`ValueError` if ``row`` can't be parsed
      :raises: :exc:`TypeError` if ``row`` is of an unknown type
   
   .. method:: __invert__()
   .. method:: inverse()
      
      Returns the inverse of a row.
      
      :return: the row's inverse
      :rtype: :class:`Row`
   
   .. method:: __pow__(n)
      
      Returns the *n*\ th power of a row.
      
      :param int n: power to which the row should be raised
      :return: result
      :rtype: :class:`Row`
   
   .. attribute:: bells
      
      Number of bells which the row contains.
   
   .. method:: make_rounds()
      
      Sets the row to rounds.
      
      :return: ``self``
      :rtype: :class:`Row`
   
   .. staticmethod:: rounds(n)
   .. staticmethod:: queens(n)
   .. staticmethod:: kings(n)
   .. staticmethod:: tittums(n)
   .. staticmethod:: reverse_rounds(n)
      
      Return the row corresponding to rounds, queens, kings, tittums and
      reverse rounds respectively on *n* bells.
      
      :param int n: number of bells
      :return: the computed row
      :rtype: :class:`Row`
   
   .. staticmethod:: pblh(n, h=1)
      
      Returns the first lead head of Plain Bob (*h* = 1), Grandsire (*h* = 2),
      or more generally the Plain Bob type method on *n* bells with *h* hunt
      bells.
      
      :param int n: number of bells
      :param int h: number of hunt bells
      :return: the computed row
      :rtype: :class:`Row`
   
   .. staticmethod:: cyclic(n, h=1, c=1)
      
      Returns a cyclic row on *n* bells with *h* initial fixed (hunt) bells. The
      variable *c* controls the number of bells moved from the front of the row
      to the end. Thus, ``Row.cyclic(6, 1, 2) == '145623'``.
      
      :param int n: number of bells
      :param int h: number of hunt bells
      :param int c: number of bells to move to the end of the row
      :return: the computed row
      :rtype: :class:`Row`
   
   .. method:: is_rounds()
      
      Determines whether the row is rounds.
      
      :return: ``True`` if the row is rounds, and ``False`` otherwise
      :rtype: boolean
   
   .. method:: is_pblh(hunts=0)
      
      If the row is a lead head of Plain Bob, Grandsire or, more generally, of
      the Plain Bob type method with any number of hunt bells, then this
      function returns an integer indicating which lead head it is. Otherwise,
      it returns ``False``.
      
      :param int hunts: number of hunt bells
      :return: lead head number, or ``False`` if not a Plain Bob-type lead head
      :rtype: int
   
   .. method:: sign()
      
      Returns the sign or parity of a row.
      
      :return: 1 for even, -1 for odd
      :rype: int
   
   .. method:: cycles()
      
      Expresses the row as separate cycles. The returned string will afterwards
      contain a list of all the cycles in the row, separated by commas; for
      example ``Row("21453678").cycles()`` will return the string
      ``"12,345,6,7,8"``.
      
      :return: representation of the row as disjoint cycles
      :rtype: string
   
   .. method:: order()
      
      Returns the order of the row.
      
      :return: the row's order
      :rtype: int
