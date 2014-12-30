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

.. class:: Change([spec[, change]])
   
   Constructs a Change.
   
   :param spec: Specification for constructing the change.
      This might be:
      
      *  Nothing. Constructs a change on zero bells.
      *  Another change. Constructs a copy.
      *  An integer number of bells. See the ``change`` parameter.
   :type spec: :class:`Change` or integer or string
   :param change: Change to read.
      This might be:
      
      *  Nothing. Constructs a change where all bells lie still (no swaps).
      *  A string (unicode or bytes) representation of a change.
   :raises: :exc:`ValueError` if a parameter can't be parsed
   :raises: :exc:`TypeError` if a parameter is of an unknown type
   
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
      :raises: :exc:`ValueError` if ``change`` can't be parsed
      :raises: :exc:`TypeError` if ``change`` is of an unknown type
   
   .. method:: set(num, pn)
      
      Sets the change to a new value.
      
      :param int num: number of bells
      :param string pn: place notation
      :return: the new change
      :rtype: :class:`Change`
      :raises: :exc:`ValueError` if a parameter can't be parsed
      :raises: :exc:`TypeError` if a parameter is of an unknown type
   
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
