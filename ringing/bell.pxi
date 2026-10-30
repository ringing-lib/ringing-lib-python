from typing import TypeAlias


cdef string symbols_string


cdef class MaxBellsDescriptor:
    def __get__(self, obj, objtype) -> int:
        return bell().MAX_BELLS


BellSpec: TypeAlias = Bell | int | str | bytes | None


cdef class Bell:
    """
    Constructs a Bell.

    Bells may be constructed in a variety of ways:

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

    * as a bell
    * as a character representing a bell
    * as an integer bell number

    If a bell parameter can't be read then a :exc:`TypeError` or
    :exc:`ValueError` exception will be raised as most appropriate.

    :param spec: Specification for constructing the bell.
        This might be:

        * Nothing. Constructs an object representing the treble (bell ``0``).
        * Another bell. Constructs a copy.
        * An integer bell number. Constructs an object representing that bell.
        * A character (``str`` or ``bytes``) representing a bell.
    :type spec: :class:`Bell` or int or string
    """

    cdef bell *thisptr

    MAX_BELLS = MaxBellsDescriptor()

    def __cinit__(self, input: BellSpec = None):
        if input is None:
            self.thisptr = new bell()
        elif isinstance(input, Bell):
            self.thisptr = new bell(int(<Bell>input))
        elif isinstance(input, int):
            if 0 <= input <= MAX_BELL_NUMBER:
                self.thisptr = new bell(<int>input)
            else:
                raise ValueError('Bell number out of range')
        elif isinstance(input, str):
            self.thisptr = new bell(
                <int>bell.read_char(ord(input.encode('ascii'))),
            )
        elif isinstance(input, bytes):
            self.thisptr = new bell(<int>bell.read_char(ord(input)))
        else:
            raise TypeError('Cannot convert {type} to ringing.Bell'.format(
                type=type(input).__name__,
            ))

    def __dealloc__(self):
        del self.thisptr

    def to_char(self) -> str:
        """
        Returns a character representing a bell:

        >>> from ringing import Bell
        >>> Bell(4).to_char()
        '5'

        :return: character
        :rtype: string
        """
        return chr(self.thisptr.to_char())

    @staticmethod
    def is_symbol(character: str | bytes) -> bool:
        """
        Checks whether a character is a valid bell symbol:

        >>> from ringing import Bell
        >>> Bell.is_symbol('5')
        True

        :param character: character to check
        :type character: string
        :return: result
        :rtype: boolean
        """
        if isinstance(character, str):
            return bell.is_symbol(ord(character.encode('ascii')))
        elif isinstance(character, bytes):
            return bell.is_symbol(ord(character))
        else:
            raise TypeError('Cannot convert {type} to str'.format(
                type=type(character).__name__,
            ))

    @staticmethod
    def set_symbols(symbols: str | bytes | None = None) -> None:
        """
        Sets the bell symbols that are to be used:

        >>> from ringing import Bell, Row
        >>> Bell.set_symbols('abcdef')
        >>> Row(6)
        Row('abcdef')
        >>> Bell.MAX_BELLS
        6

        Note that bell symbols are set on a global level.
        Omit the symbol specification in order to reset to the default symbols:

        >>> from ringing import Bell, Row
        >>> Bell.set_symbols('abcdef')
        >>> Row(6)
        Row('abcdef')
        >>> Bell.set_symbols()
        >>> Row(6)
        Row('123456')

        :param symbols: symbols to use
        :type symbols: string
        """
        global symbols_string

        if symbols is None:
            bell.set_symbols(NULL)
        elif isinstance(symbols, str):
            symbols_string = <string>(symbols.encode('ascii'))
            bell.set_symbols(symbols_string.c_str())
        elif isinstance(symbols, bytes):
            symbols_string = <string>symbols
            bell.set_symbols(symbols_string.c_str())
        else:
            raise TypeError('Cannot convert {type} to str'.format(
                type=type(symbols).__name__,
            ))

    def __richcmp__(self, other, int op) -> bool:
        cdef int bx
        cdef int by

        bx = int(self)

        try:
            by = int(Bell(other))
        except TypeError:
            return NotImplemented

        if op == 0:  # <
            return bx < by
        elif op == 1:  # <=
            return bx <= by
        elif op == 2:  # ==
            return bx == by
        elif op == 3:  # !=
            return bx != by
        elif op == 4:  # >
            return bx > by
        elif op == 5:  # >=
            return bx >= by

    def __str__(self) -> str:
        if self < Bell.MAX_BELLS:
            return self.to_char()
        else:
            return '{{{bell:d}}}'.format(bell=int(self) + 1)

    def __bytes__(self) -> bytes:
        return str(self).encode('ascii')

    def __repr__(self) -> str:
        return f'Bell({int(self):d})'

    def __int__(self) -> int:
        return <int>deref(self.thisptr)
