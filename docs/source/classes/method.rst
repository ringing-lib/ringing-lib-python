Methods
=======

.. currentmodule:: ringing

The Ringing Class Library provides many useful functions for dealing with
methods, finding information about them and classifying them.

A *method* consists of one block of changes which is repeated over and over
again; this is called a *lead*. If, at the end of one lead, every bell is in a
different position, then the method is called a *principle* and the leads are
called *divisions*. Any bells in a method which end up in the same place at the
end of a lead are called *hunt bells*.

The Ringing Class Library defines a :class:`Method` object which is simply a
block of changes and which provides a large range of member functions. Many of
these are used for finding out things about the method, such as the number of
leads in the plain course, the type of method, the full name and so on.

The Method Class
----------------

The :class:`Method` class represents a method by storing the changes which make
up one lead of the method.

A method may have a name, which is a string variable. This name is the *base
name* of the method, that is, it is the name without any extra bits such as
"Surprise" or "Triples". For example, the base name of Plain Bob Major is simply
"Plain". The parts of the name other than the base can be worked out by the
Ringing Class Library.

.. autoclass:: Method(input: Method | int | str | bytes | None = None, bells: int = 0, name: str = 'Untitled')

   .. method:: __lt__(method)
   .. method:: __le__(method)
   .. method:: __eq__(method)
   .. method:: __ne__(method)
   .. method:: __gt__(method)
   .. method:: __ge__(method)

      Compares a method to another.

      :param method: value to compare
      :type method: :class:`Method`
      :return: result
      :rtype: boolean

   .. autoattribute:: size
   .. autoattribute:: length
   .. autoattribute:: bells
   .. autoattribute:: name
   .. automethod:: append
   .. automethod:: lead_head
   .. automethod:: leads
   .. automethod:: is_regular
   .. automethod:: lh_code
   .. automethod:: hunt_bells
   .. automethod:: is_symmetric
   .. automethod:: is_palindromic
   .. automethod:: is_double
   .. automethod:: max_blows
   .. automethod:: is_plain
   .. automethod:: has_dodges
   .. automethod:: has_places
   .. automethod:: full_name
   .. automethod:: stage_name
   .. automethod:: format
