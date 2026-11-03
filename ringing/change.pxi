from typing import Literal, TypeAlias


ChangeSpec: TypeAlias = Change | int | None


cdef class Change:
    """
    Constructs a Change.

    Changes may be constructed in a variety of ways:

    >>> from ringing import Change
    >>> Change(12)  # an empty change from an integer bell number
    Change(12, '1234567890ET')
    >>> Change(12, 'x')  # a specific change on a number of bells
    Change(12, 'X')
    >>> Change(Change(12))  # from another change
    Change(12, '1234567890ET')

    Once changes are created they can be modified by swapping pairs.

    :param spec: Specification for constructing the change.
        This might be:

        * Nothing. Constructs a change on zero bells.
        * Another change. Constructs a copy.
        * An integer number of bells. See the ``change`` parameter.
    :type spec: :class:`Change` or int or string
    :param change: Change to read.
        This might be:

        * Nothing. Constructs a change where all bells lie still (no swaps).
        * A string (``str`` or ``bytes``) representation of a change.
    """

    cdef change *thisptr

    def __cinit__(
        self,
        input: ChangeSpec = None,
        change_str: str | bytes | None = None,
    ):
        if input is None:
            self.thisptr = new change()
        elif isinstance(input, Change):
            self.thisptr = new change(deref((<Change>input).thisptr))
        elif isinstance(input, int):
            if 0 <= input <= MAX_BELL_NUMBER:
                if change_str is None:
                    self.thisptr = new change(<int>input)
                elif isinstance(change_str, str):
                    self.thisptr = new change(
                        <int>input,
                        <string>(change_str.encode('ascii')),
                    )
                elif isinstance(change_str, bytes):
                    self.thisptr = new change(<int>input, <string>change_str)
                else:
                    raise TypeError('Cannot convert {type} to str'.format(
                        type=type(change_str).__name__,
                    ))
            else:
                raise ValueError('Number of bells out of range')
        else:
            raise TypeError('Cannot convert {type} to ringing.Change'.format(
                type=type(input).__name__,
            ))

    def __dealloc__(self):
        del self.thisptr

    def set(self, int num, pn: str | bytes) -> None:
        """
        Sets the change to a new value.

        :param int num: number of bells
        :param string pn: place notation
        :return: ``None``
        """
        if 0 <= num <= MAX_BELL_NUMBER:
            if isinstance(pn, bytes):
                self.thisptr.set(num, pn)
            elif isinstance(pn, str):
                self.thisptr.set(num, pn.encode('ascii'))
            else:
                raise TypeError('Cannot convert {type} to str'.format(
                    type=type(pn).__name__,
                ))
        else:
            raise ValueError('Number of bells out of range')

    def reverse(self) -> Change:
        """
        Returns the reverse of a change; that is, the change is flipped over so
        that on 8 bells for example, 2nds place becomes 7ths place and so on.

        :return: result
        :rtype: :class:`Change`
        """
        cdef Change result = Change()
        result.thisptr[0] = self.thisptr.reverse()
        return result

    @property
    def bells(self) -> int:
        """
        Number of bells on which the change is defined.
        """
        return self.thisptr.bells()

    def sign(self) -> Literal[+1, -1]:
        """
        Returns the sign of the change.

        :return: -1 if an odd number of pairs are swapped, +1 if an even number
            of pairs are swapped
        :rtype: int
        """
        return self.thisptr.sign()

    def find_swap(self, b: BellSpec) -> bool:
        """
        Determines whether a position is swapped by the change.

        :param b: position to check
        :type b: :class:`Bell` or string or int
        :return: ``True`` if the change swaps positions *b* and *b*\ +1, and
            ``False`` otherwise
        :rtype: boolean
        :raises: :exc:`IndexError` if ``b`` is out of range
        """
        cdef bell bb = deref(Bell(b).thisptr)
        if <int>bb < (self.thisptr.bells() - 1):
            return self.thisptr.findswap(bb)
        else:
            raise IndexError('ringing.Change index out of range')

    def find_place(self, b: BellSpec) -> bool:
        """
        Determines whether a place is made.

        :param b: position to check
        :type b: :class:`Bell` or string or int
        :return: ``True`` if the change doesn't move the bell in the *b*\ th
            place (i.e. if *b*\ ths place is made), and ``False`` otherwise
        :rtype: boolean
        :raises: :exc:`IndexError` if ``b`` is out of range
        """
        cdef bell bb = deref(Bell(b).thisptr)
        if <int>bb <= (self.thisptr.bells() - 1):
            return self.thisptr.findplace(bb)
        else:
            raise IndexError('ringing.Change index out of range')

    def swap_pair(self, b: BellSpec) -> bool:
        """
        If the change doesn't currently swap positions *b* and *b*\ +1, then
        this will add that swap. If those positions are swapped, this will
        remove the swap. If the positions *b*\ -1 and *b*, or *b*\ +1 and
        *b*\ +2, are currently swapped, those swaps are removed.

        This function makes it possible for the user to edit changes in such a
        way that they will always end up in a sensible state.

        :param b: position to check
        :type b: :class:`Bell` or string or int
        :return: ``True`` if after the function call, the pair of positions *b*
            and *b*\ +1 are swapped, and ``False`` otherwise
        :rtype: boolean
        :raises: :exc:`IndexError` if ``b`` is out of range
        """
        cdef bell bb = deref(Bell(b).thisptr)
        return self.thisptr.swappair(bb)

    def internal(self) -> bool:
        """
        Checks whether the change contains internal places.

        :return: ``True`` if the change contains internal places, and ``False``
            otherwise
        :rtype: boolean
        """
        return self.thisptr.internal()

    def count_places(self) -> int:
        """
        Returns the number of places made in the change

        :return: number of places made
        :rtype: int
        """
        return self.thisptr.count_places()

    def __richcmp__(self, other, int op) -> bool:
        cdef change cx
        cdef change cy

        cx = deref((<Change>self).thisptr)

        if isinstance(other, Change):
            cy = deref(Change(other).thisptr)
        elif isinstance(other, bytes) or isinstance(other, str):
            cy = deref(Change(self.bells, other).thisptr)
        else:
            return NotImplemented

        if op == 0:  # <
            return cx < cy
        elif op == 1:  # <=
            return cx <= cy
        elif op == 2:  # ==
            return cx == cy
        elif op == 3:  # !=
            return cx != cy
        elif op == 4:  # >
            return cx > cy
        elif op == 5:  # >=
            return cx >= cy

    def __str__(self) -> str:
        return self.thisptr.print().decode('ascii')

    def __bytes__(self) -> bytes:
        return self.thisptr.print()

    def __repr__(self) -> str:
        if self.thisptr.bells():
            return f"Change({self.thisptr.bells()}, '{self}')"
        else:
            return 'Change()'

    def __mul__(self, other) -> Bell:
        """
        Returns the effect of applying the change to the bell *b*\ . This is
        useful in tracing the path of one particular bell through a series of
        changes.

        >>> from ringing import Change
        >>> 3 * Change(4, '34')
        Bell(3)
        >>> [Change(4, '34') * b for b in range(4)]
        [Bell(1), Bell(0), Bell(2), Bell(3)]

        :param bell: bell to apply
        :type bell: :class:`Bell` or string or int
        :return: result
        :rtype: int
        :raises: :exc:`ValueError` if ``bell`` is out of range
        """
        cdef bell b
        cdef change c

        c = deref((<Change>self).thisptr)

        # Special handling for integers because returning NotImplemented will
        # yield an error message saying the type is incorrect; the type may be
        # correct but the value out of range.
        if isinstance(other, int) and (other < 0 or other > MAX_BELL_NUMBER):
            raise ValueError('Bell number out of range')

        # Ordinary case: try to convert parameter to Bell.
        try:
            b = deref(Bell(other).thisptr)
        except:
            return NotImplemented

        return Bell(<int>(b * c))

    def __rmul__(self, other) -> Bell:
        return Change.__mul__(self, other)
