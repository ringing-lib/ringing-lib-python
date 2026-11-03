Changes
=======

.. currentmodule:: ringing

A *change* is a means for getting from one row to another. It works by swapping
over pairs of bells, and no bell may move more than one place.

The normal way of representing a change is by place notation; a single change is
represented by a series of numbers which each correspond to a place being made;
for example, ``12`` means that all bells swap, apart from the 1 and the 2, which
stay in the same place. If all the bells swap, the place notation is ``X``.

The Change Class
----------------

.. autoclass:: Change(input: Change | int | None = None, change: str | bytes | None = None)

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

   .. automethod:: __mul__(bell: Bell | int | str | bytes) -> Bell
   .. automethod:: set
   .. automethod:: reverse
   .. autoattribute:: bells
   .. automethod:: sign
   .. automethod:: find_swap
   .. automethod:: find_place
   .. automethod:: swap_pair
   .. automethod:: internal
   .. automethod:: count_places


Blocks of Rows
--------------

The :class:`RowBlock` class is an array of rows which has associated with it a
reference to an array of changes, and can recalculate itself from those changes.
For example, suppose that the variable *c*, a list of changes, holds one lead of
a method; then it is possible to define a variable of type :class:`RowBlock`
which, once it is told what the lead head is, will calculate the rows for one
lead of the method.

.. autoclass:: RowBlock(changes, [starting_row])

   .. autoattribute:: size
   .. autoattribute:: changes
   .. automethod:: set_start
   .. automethod:: recalculate
