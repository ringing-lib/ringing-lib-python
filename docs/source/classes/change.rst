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
      :raises: :exc`TypeError` if ``change`` is of an unknown type
   
   .. attribute:: bells
      
      Number of bells on which the change is defined.
