Changes
=======

A *change* is a means for getting from one row to another. It works by swapping
over pairs of bells, and no bell may move more than one place.

The normal way of representing a change is by place notation; a single change is
represented by a series of numbers which each correspond to a place being made;
for example, ``12`` means that all bells swap, apart from the 1 and the 2, which
stay in the same place. If all the bells swap, the place notation is ``X``.

The Change Class
----------------

.. currentmodule:: ringing

.. class:: Change([spec[, change]])
   
   Constructs a Change.
   
   :param spec: Specification for constructing the change.
      This might be:
      
      *  Nothing. Constructs a change on zero bells.
      *  Another change. Constructs a copy.
      *  An integer number of bells. See the ``change`` parameter.
   :type spec: :class:`Change` or int or string
   :param change: Change to read.
      This might be:
      
      *  Nothing. Constructs a change where all bells lie still (no swaps).
      *  A string (unicode or bytes) representation of a change.
   
   .. method:: __lt__(change)
   .. method:: __le__(change)
   .. method:: __eq__(change)
   .. method:: __ne__(change)
   .. method:: __gt__(change)
   .. method:: __ge__(change)
      
      Compare a change to another.
      
      :param change: value to compare; strings are parsed as changes on the same
         number of bells
      :type change: :class:`Change` or string
      :return: result
      :rtype: boolean
   
   .. method:: __mul__(bell)
      
      Returns the effect of applying the change to the bell *b*\ . For example,
      ``3 * Change(4, '34') == 3``. This is useful in tracing the path of one
      particular bell through a series of changes.
      
      :param int bell: bell to apply
      :return: result
      :rtype: int
      :raises: :exc:`ValueError` if ``bell`` is out of range
   
   .. method:: set(num, pn)
      
      Sets the change to a new value.
      
      :param int num: number of bells
      :param string pn: place notation
      :return: ``None``
   
   .. method:: reverse()
      
      Returns the reverse of a change; that is, the change is flipped over so
      that on 8 bells for example, 2nds place becomes 7ths place and so on.
      
      :return: result
      :rtype: :class:`Change`
   
   .. attribute:: bells
      
      Number of bells on which the change is defined.
   
   .. method:: sign()
      
      Returns the sign of the change.
      
      :return: -1 if an odd number of pairs are swapped, +1 if an even number of
         pairs are swapped
      :rtype: int
   
   .. method:: find_swap(i)
      
      Determines whether a position is swapped by the change.
      
      :param int i: zero-indexed place to check
      :return: ``True`` if the change swaps bells *i* and *i*\ +1, and ``False``
         otherwise
      :rtype: boolean
      :raises: :exc:`IndexError` if ``i`` is out of range
   
   .. method:: find_place(i)
      
      Determines whether a place is made.
      
      :param int i: zero-indexed place to check
      :return: ``True`` if the change doesn't move the bell in the *i*\ th place
         (i.e. if *i*\ ths place is made), and ``False`` otherwise
      :rtype: boolean
      :raises: :exc:`IndexError` if ``i`` is out of range
   
   .. method:: swap_pair(i)
      
      If the change doesn't currently swap bells *i* and *i*\ +1, then this will
      add that swap. If those bells are swapped, this will remove the swap. If
      the bells *i*\ -1 and *i*, or *i*\ +1 and *i*\ +2, are currently swapped,
      those swaps are removed.
      
      This function makes it possible for the user to edit changes in such a way
      that they will always end up in a sensible state.
      
      :param int i: zero-indexed place to swap
      :return: ``True`` if after the function call, the pair of bells *i* and
         *i*\ +1 are swapped, and ``False`` otherwise
      :rtype: boolean
      :raises: :exc:`IndexError` if ``i`` is out of range
   
   .. method:: internal()
      
      Checks whether the change contains internal places.
      
      :return: ``True`` if the change contains internal places, and ``False``
         otherwise
      :rtype: boolean
   
   .. method:: count_places()
      
      Returns the number of places made in the change
      
      :return: number of places made
      :rtype: int

Blocks of Rows
--------------

The :class:`RowBlock` class is an array of rows which has associated with it a
reference to an array of changes, and can recalculate itself from those changes.
For example, suppose that the variable *c*, a list of changes, holds one lead of
a method; then it is possible to define a variable of type :class:`RowBlock`
which, once it is told what the lead head is, will calculate the rows for one
lead of the method.

.. class:: RowBlock(changes, [starting_row])
   
   Creates a block of rows using the changes in *changes*, starting from the row
   given in *starting_row* (or rounds if *starting_row* is not provided).
   
   Row blocks support several standard sequence operations::
      
      >>> from ringing import RowBlock, Change
      >>> rb = RowBlock([Change(5, '3'), Change(5, '1'), Change(5, '5')])
      >>> rb[0]
      Row('12345')
      >>> for r in rb:
      ...     print(r)
      ...
      12345
      21354
      23145
      32415
   
   ========================  ==================================================
   Operation                 Result
   ========================  ==================================================
   ``r in rb``               ``True`` if an item of *rb* is equal to *r*, else
                             ``False``
   ``r not in rb``           ``False`` if an item of *rb* is equal to *r*, else
                             ``True``
   ``rb[i]``                 *i*\ th row of *rb*, origin 0
   ``rb[i] = Row('12345')``  sets *i*\ th row of *rb*
   ``len(rb)``               length (:attr:`size`) of *rb*
   ``list(rb)``              list of rows in *rb*
   ========================  ==================================================
   
   :param changes: changes to associate with the block
   :type changes: [:class:`Change`]
   :param starting_row: optional starting row
   :type starting_row: :class:`Row`
   
   .. attribute:: size
      
      Number of rows which the row block contains::
         
         >>> from ringing import RowBlock, Change
         >>> rb = RowBlock([Change(5, '3'), Change(5, '1'), Change(5, '5')])
         >>> rb.size
         4
   
   .. attribute:: changes
      
      List of changes associated with the row block::
         
         >>> from ringing import RowBlock, Change
         >>> rb = RowBlock([Change(5, '3'), Change(5, '1'), Change(5, '5')])
         >>> rb.changes
         [Change(5, '3'), Change(5, '1'), Change(5, '5')]
      
      It's also possible to assign a new set of changes::
         
         >>> from ringing import RowBlock, Change
         >>> rb = RowBlock([Change(5, '3'), Change(5, '1'), Change(5, '5')])
         >>> list(rb)
         [Row('12345'), Row('21354'), Row('23145'), Row('32415')]
         >>> rb.changes = [Change(5, pn) for pn in ['5', '3']]
         >>> list(rb)
         [Row('12345'), Row('21435'), Row('12453')]
   
   .. method:: set_start(starting_row)
      
      Assigns a new row for the start of the row block.
      Other rows remain unmodified; call :meth:`recalculate` to update them::
         
         >>> from ringing import RowBlock, Change
         >>> rb = RowBlock([Change(5, '3'), Change(5, '1'), Change(5, '5')])
         >>> list(rb)
         [Row('12345'), Row('21354'), Row('23145'), Row('32415')]
         >>> rb.set_start('54321')
         >>> list(rb)
         [Row('54321'), Row('21354'), Row('23145'), Row('32415')]
         >>> rb.recalculate()
         >>> list(rb)
         [Row('54321'), Row('45312'), Row('43521'), Row('34251')]
      
      :param starting_row: new starting row
      :type starting_row: :class:`Row` or int or string
      :return: ``None``
   
   .. method:: recalculate([start])
      
      Recalculates the rows within the row block::
         
         >>> from ringing import RowBlock, Change
         >>> rb = RowBlock([Change(5, '3'), Change(5, '1'), Change(5, '5')])
         >>> list(rb)
         [Row('12345'), Row('21354'), Row('23145'), Row('32415')]
         >>> rb[2] = '54321'
         >>> list(rb)
         [Row('12345'), Row('21354'), Row('54321'), Row('32415')]
         >>> rb.recalculate(2)
         >>> list(rb)
         [Row('12345'), Row('21354'), Row('54321'), Row('45231')]
      
      :param int start: if supplied, only rows after this index will be
         recalculated
      :return: ``None``
      :raises: :exc:`IndexError` if ``start`` is out of range
