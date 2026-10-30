Bells
=====

.. currentmodule:: ringing

The :class:`Bell` class represents a single bell. An object of type
:class:`Bell` is essentially an integer, and bells are numbered starting with
the treble as ``0``. Member functions are provided to convert between this
numerical representation and a printable character. The class library can cope
with up to 256 bells, though only bells numbered from 0 to 32 may be described
by a printable character.

.. autoclass:: Bell(input: :class:`Bell` | int | str | bytes | None = None)

   .. method:: __lt__(bell)
   .. method:: __le__(bell)
   .. method:: __eq__(bell)
   .. method:: __ne__(bell)
   .. method:: __gt__(bell)
   .. method:: __ge__(bell)

      Compare a bell to another::

         >>> from ringing import Bell
         >>> Bell(4) == '5'
         True

      :param bell: value to compare
      :type bell: :class:`Bell` or int or string
      :return: result
      :rtype: boolean

   .. attribute:: MAX_BELLS

      Maximum number of bells that may be represented using symbols.
      If the number of bells exceeds this value, the extra bells will be shown
      as "``*``" characters.

      This attribute is available on the class as well as instances of it::

         >>> from ringing import Bell
         >>> Bell.MAX_BELLS
         33
         >>> Bell(32).to_char()
         'Z'
         >>> Bell(33).to_char()
         '*'

      :type: integer

   .. automethod:: to_char
   .. automethod:: is_symbol
   .. automethod:: set_symbols
