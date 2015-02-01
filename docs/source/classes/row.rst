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

.. class:: Row([spec])
   
   Constructs a Row.
   
   Rows may be constructed in a variety of ways::
      
      >>> from ringing import Row
      >>> Row(4)  # from an integer number of bells
      Row('1234')
      >>> Row('1234')  # from a string containing the row
      Row('1234')
      >>> Row(Row('1234'))  # from another row
      Row('1234')
   
   Rows are immutable once created.
   
   This library makes extensive use of :class:`Row` objects as function
   parameters.
   These may be passed in the same ways:
   
   *  as a row
   *  as a string containing the row
   *  as an integer number of bells
   
   If a row parameter can't be read then a :exc:`TypeError` or :exc:`ValueError`
   exception will be raised as most appropriate.
   
   :param spec: Specification for constructing the row.
      This might be:
      
      *  Nothing. Constructs a row on zero bells.
      *  Another row. Constructs a copy.
      *  An integer number of bells. Constructs rounds.
      *  A string (unicode or bytes) representation of a row.
   :type spec: :class:`Row` or int or string
   
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
   
   .. method:: __getitem__(i)
      
      This returns the *i*\ th bell in the row::
         
         >>> from ringing import Row
         >>> r = Row('512364')
         >>> r[0]
         4
         >>> r[1]
         0
         >>> print([b for b in r])
         [4, 0, 1, 2, 5, 3]
      
      .. note::
         
         Note that this is not an lvalue,
         so you cannot assign a value to an individual bell in a row.
      
      :param int i: bell position to return (0-indexed)
      :return: bell number in that position (0-indexed; ``0`` is the treble)
      :rtype: int
   
   .. method:: __mul__(row)
      
      Multiplies two rows together as explained above::
         
         >>> from ringing import Row
         >>> r = Row('21345678')
         >>> r * '13572468'
         Row('23571468')
         >>> '13572468' * r
         Row('31572468')
      
      If the rows are not of the same length, the shorter row is considered to
      be first padded out to the length of the longer row by adding the extra
      bells in order at the end.
      
      :param row: value to multiply by
      :type row: :class:`Row` or int or string
      :return: result
      :rtype: :class:`Row`
   
   .. method:: __mul__(change)
      
      Applies a change to a row::
         
         >>> from ringing import Row, Change
         >>> Row('214365') * Change(6, '1')
         Row('241635')
      
      If the number of bells *c* differs from the number of bells in *r*\ , then
      *c* is considered to be padded or truncated in the obvious way.
      
      :param change: change to apply
      :type change: :class:`Change`
      :return: result
      :rtype: :class:`Row`
   
   .. method:: __div__(row)
      
      Divides two rows, as explained above::
         
         >>> from ringing import Row
         >>> Row('23571468') / Row('13572468')
         Row('21345678')
      
      If the rows are not of the same length, the shorter row is considered to
      be first padded out to the length of the longer row by adding the extra
      bells in order at the end.
      
      :param row: value to divide by
      :type row: :class:`Row` or int or string
      :return: result
      :rtype: :class:`Row`
   
   .. method:: __invert__()
   .. method:: inverse()
      
      Returns the inverse of a row::
         
         >>> from ringing import Row
         >>> r = Row('13572468')
         >>> ~r
         Row('15263748')
         >>> r.inverse()
         Row('15263748')
         >>> r * ~r
         Row('12345678')
         >>> ~r * r
         Row('12345678')
      
      :return: the row's inverse
      :rtype: :class:`Row`
   
   .. method:: __pow__(n)
      
      Returns the *n*\ th power of a row::
         
         >>> from ringing import Row
         >>> r = Row('13572468')
         >>> r ** 0
         Row('12345678')
         >>> r ** 1
         Row('13572468')
         >>> r ** 2
         Row('15263748')
         >>> r ** 3
         Row('12345678')
      
      :param int n: power to which the row should be raised
      :return: result
      :rtype: :class:`Row`
   
   .. attribute:: bells
      
      Number of bells which the row contains::
         
         >>> from ringing import Row
         >>> Row('2143').bells
         4
   
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
   
   .. staticmethod:: pblh(n, [h=1])
      
      Returns the first lead head of Plain Bob (*h* = 1), Grandsire (*h* = 2),
      or more generally the Plain Bob type method on *n* bells with *h* hunt
      bells::
         
         >>> from ringing import Row
         >>> Row.pblh(6)
         Row('135264')
      
      :param int n: number of bells
      :param int h: number of hunt bells
      :return: the computed row
      :rtype: :class:`Row`
   
   .. staticmethod:: cyclic(n, [h=1], [c=1])
      
      Returns a cyclic row on *n* bells with *h* initial fixed (hunt) bells. The
      variable *c* controls the number of bells moved from the front of the row
      to the end::
         
         >>> from ringing import Row
         >>> Row.cyclic(6, 1, 2)
         Row('145623')
      
      :param int n: number of bells
      :param int h: number of hunt bells
      :param int c: number of bells to move to the end of the row
      :return: the computed row
      :rtype: :class:`Row`
   
   .. method:: is_rounds()
      
      Determines whether the row is rounds::
         
         >>> from ringing import Row
         >>> Row('12345678').is_rounds()
         True
         >>> Row('72635184').is_rounds()
         False
      
      :return: ``True`` if the row is rounds, and ``False`` otherwise
      :rtype: boolean
   
   .. method:: is_pblh([hunts=0])
      
      If the row is a lead head of Plain Bob, Grandsire or, more generally, of
      the Plain Bob type method with any number of hunt bells, then this
      function returns an integer indicating which lead head it is. Otherwise,
      it returns ``False``.
      
      :param int hunts: number of hunt bells
      :return: lead head number, or ``False`` if not a Plain Bob-type lead head
      :rtype: int
   
   .. method:: sign()
      
      Returns the sign or parity of a row::
         
         >>> from ringing import Row
         >>> Row('12345678').sign()
         1
         >>> Row('21345678').sign()
         -1
      
      :return: 1 for even, -1 for odd
      :rype: int
   
   .. method:: cycles()
      
      Expresses the row as separate cycles. The returned string will afterwards
      contain a list of all the cycles in the row, separated by commas::
         
         >>> from ringing import Row
         >>> Row('21453678').cycles()
         '12,345,6,7,8'
      
      :return: representation of the row as disjoint cycles
      :rtype: string
   
   .. method:: order()
      
      Returns the order of the row::
         
         >>> from ringing import Row
         >>> r = Row('21453678')
         >>> r.order()
         6
         >>> (r ** 6).is_rounds()
         True
      
      :return: the row's order
      :rtype: int
   
   .. method:: find(b)
      
      Locates the bell, *b*, in this row and returns its place::
         
         >>> from ringing import Row
         >>> r = Row('512364')
         >>> r.find(0)
         1
         >>> r.find(1)
         2
      
      See also :meth:`__getitem__`.
      
      :param int b: bell number to find (0-indexed; ``0`` is the treble)
      :return: bell position (0-indexed)
      :rtype: int
   
   .. staticmethod:: conjugator(x, y)
      
      Two rows, *x* and *y*, are conjugate if there exists some row, *r*, such
      that::
         
         y = (r ^ -1) . x . r
      
      or, in Python::
         
         y = ~r * x * r
      
      If *x* and *y* are conjugate, this method computes the row *r* that
      relates them.
      
      :param x: row ``x``
      :type x: :class:`Row` or int or string
      :param y: row ``y``
      :type y: :class:`Row` or int or string
      :return: row ``r``, or ``None`` if the rows are not conjugate
      :rtype: :class:`Row` or ``None``
   
   .. staticmethod:: are_conjugate(x, y)
      
      Determines whether the rows *x* and *y* are conjugate as described above.
      
      :param x: row ``x``
      :type x: :class:`Row` or int or string
      :param y: row ``y``
      :type y: :class:`Row` or int or string
      :return: ``True`` if the rows are conjugate, or ``False`` otherwise
      :rtype: boolean

The Group Class
---------------

.. class:: Group(generator[, generator[, ...]])
   
   Generates a group of rows.
   
   Once created, groups can be tested for membership or iterated over using the
   ``in`` operator (and hence converted to lists via ``list()``).
   Groups are immutable.
   
   :param generator: generators for the group (rows)
   :type generator: :class:`Row` or int or string
   
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
   
   .. attribute:: bells
      
      Number of bells which the group's rows contain::
         
         >>> from ringing import Group
         >>> Group('2143', '1324').bells
         4
   
   .. attribute:: size
      
      Number of rows which the group contains (the *order* of the group)::
         
         >>> from ringing import group
         >>> Group('2143', '1324').size
         8
   
   .. staticmethod:: symmetric_group(working_bells[, hunt_bells[, total_bells]])
   .. staticmethod:: alternating_group(working_bells[, hunt_bells[, total_bells]])
      
      Returns the symmetric or alternating group respectively.
      
      The symmetric group S\ :sub:`n` contains all permutations on *n* bells,
      i.e. the extent.
      The alternating group A\ :sub:`n` contains all even permutations on *n*
      bells (see :meth:`Row.sign`).
      
      By specifying *hunt_bells* and *total_bells* it's possible to produce
      groups with more fixed bells, e.g.::
         
         >>> from ringing import Group
         >>> list(Group.alternating_group(3, 1, 8))
         [Row('12345678'), Row('13425678'), Row('14235678')]
      
      :param int working_bells: *n*, number of bells involved in permutations
      :param int hunt_bells: number of fixed bells at the start of the change
      :param int total_bells: number of bells in each row
      :return: the computed group
      :rtype: :class:`Group`
      :raises: :exc:`ValueError` if *total_bells* is less than the sum of
         *working_bells* and *hunt_bells*
   
   .. method:: conjugate(r)
      
      Conjugates the group by a row *r*, in pseudocode::
         
         H = (r ^ -1) . g . r for g in G
      
      :param r: row *r*
      :type r: :class:`Row` or int or string
      :return: the computed group
      :rtype: :class:`Group`
   
   .. method:: rcoset_label(r)
   .. method:: lcoset_label(r)
      
      A subgroup H of S\ :sub:`n` partitions the group into ``n! / |G|`` cosets.
      
      *  *g*\ H is the left coset of H in G with respect to *g*
      *  H\ *g* is the right coset of H in G with respect to *g*
      
      Each coset may be conveniently labelled by choosing the lexicographically
      least element within it.
      
      These methods return the label of the right or left coset (respectively)
      of G in S\ :sub:`n` with respect to the row *r*.
      
      :param r: row *r*
      :type r: :class:`Row` or int or string
      :return: the computed label
      :rtype: :class:`Row`
   
   .. method:: invariants
      
      Returns a list of invariant bells as 0-indexed integers, e.g.::
         
         >>> from ringing import Group
         >>> Group.alternating_group(3, 1, 8).invariants()
         [0, 4, 5, 6, 7]
      
      :return: invariant bells
      :rtype: [int]
