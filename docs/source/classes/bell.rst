Bells
=====

.. currentmodule:: ringing

The :class:`Bell` class represents a single bell. An object of type
:class:`Bell` is essentially an integer, and bells are numbered starting with
the treble as ``0``. Member functions are provided to convert between this
numerical representation and a printable character. The class library can cope
with up to 256 bells, though only bells numbered from 0 to 32 may be described
by a printable character.

.. class:: Bell([spec])
   
   Constructs a Bell.
   
   Bells may be constructed in a variety of ways::
      
      >>> from ringing import Bell
      >>> Bell(10)  # from an integer bell number
      Bell(10)
      >>> Bell('E')  # from a printable character
      Bell(10)
      >>> Bell(Bell(10))  # from another bell
      Bell(10)
   
   Bells are immutable once created.
   
   This library makes extensive use of :class:`Bell` objects as function
   parameters.
   These may be passed in the same ways:
   
   *  as a bell
   *  as a character representing a bell
   *  as an integer bell number
   
   If a bell parameter can't be read then a :exc:`TypeError` or
   :exc:`ValueError` exception will be raised as most appropriate.
   
   :param spec: Specification for constructing the bell.
      This might be:
      
      *  Nothing. Constructs an object representing the treble (bell ``0``).
      *  Another bell. Constructs a copy.
      *  An integer bell number. Constructs an object representing that bell.
      *  A character (unicode or bytes) representing a bell.
   :type spec: :class:`Bell` or int or string
   
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
      
      :param row: value to compare
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
   
   .. method:: to_char()
      
      Returns a character representing a bell::
         
         >>> from ringing import Bell
         >>> Bell(4).to_char()
         '5'
      
      :return: character
      :rtype: string
   
   .. staticmethod:: is_symbol(character)
      
      Checks whether a character is a valid bell symbol::
         
         >>> from ringing import Bell
         >>> Bell.is_symbol('5')
         True
      
      :param character: character to check
      :type character: string
      :return: result
      :rtype: boolean
   
   .. staticmethod:: set_symbols([symbols])
      
      Sets the bell symbols that are to be used::
         
         >>> from ringing import Bell, Row
         >>> Bell.set_symbols('abcdef')
         >>> Row(6)
         Row('abcdef')
         >>> Bell.MAX_BELLS
         6
      
      Note that bell symbols are set on a global level.
      Omit the symbol specification in order to reset to the default symbols::
         
         >>> from ringing import Bell, Row
         >>> Bell.set_symbols('abcdef')
         >>> Row(6)
         Row('abcdef')
         >>> Bell.set_symbols()
         >>> Row(6)
         Row('123456')
      
      :param symbols: symbols to use
      :type symbols: string
