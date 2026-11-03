from typing import Literal, TypeAlias


RowSpec: TypeAlias = Row | int | str | bytes | None


cdef class Row:
    """
    Constructs a Row.

    Rows may be constructed in a variety of ways:

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

    * as a row
    * as a string containing the row
    * as an integer number of bells

    If a row parameter can't be read then a :exc:`TypeError` or
    :exc:`ValueError` exception will be raised as most appropriate.

    :param input: Specification for constructing the row.
        This might be:

        * Nothing. Constructs a row on zero bells.
        * Another row. Constructs a copy.
        * An integer number of bells. Constructs rounds.
        * A string (``str`` or ``bytes``) representation of a row.
    :type input: :class:`Row` or int or string
    """

    cdef row *thisptr

    def __cinit__(self, input: RowSpec = None):
        if input is None:
            self.thisptr = new row()
        elif isinstance(input, Row):
            self.thisptr = new row(deref((<Row>input).thisptr))
        elif isinstance(input, int):
            if 0 <= input <= MAX_BELL_NUMBER:
                self.thisptr = new row(<int>input)
            else:
                raise ValueError('Number of bells out of range')
        elif isinstance(input, str):
            self.thisptr = new row(<string>(input.encode('ascii')))
        elif isinstance(input, bytes):
            self.thisptr = new row(<string>input)
        else:
            raise TypeError('Cannot convert {type} to ringing.Row'.format(
                type=type(input).__name__,
            ))

    def __dealloc__(self):
        del self.thisptr

    def inverse(self) -> Row:
        """
        Returns the inverse of a row:

        >>> from ringing import Row
        >>> r = Row('13572468')
        >>> r.inverse()
        Row('15263748')

        :return: the row's inverse
        :rtype: :class:`Row`
        """
        cdef Row result = Row()
        result.thisptr[0] = self.thisptr.inverse()
        return result

    @property
    def bells(self) -> int:
        """
        Number of bells which the row contains:

        >>> from ringing import Row
        >>> Row('2143').bells
        4
        """
        return self.thisptr.bells()

    def conjugate(self, r: RowSpec) -> Row:
        """
        Conjugates the row by another row *r*, in pseudocode::

            R = (r ^ -1) . self . r

        :param r: row *r*
        :type r: :class:`Row` or int or string
        :return: the computed row
        :rtype: :class:`Row`
        """
        cdef Row result = Row()
        result.thisptr[0] = self.thisptr.conjugate(deref(Row(r).thisptr))
        return result

    @staticmethod
    def rounds(int n) -> Row:
        """
        Returns the row corresponding to rounds on *n* bells.

        :param int n: number of bells
        :return: the computed row
        :rtype: :class:`Row`
        """
        cdef Row result = Row()
        result.thisptr[0] = row.rounds(n)
        return result

    @staticmethod
    def queens(int n) -> Row:
        """
        Returns the row corresponding to queens on *n* bells.

        :param int n: number of bells
        :return: the computed row
        :rtype: :class:`Row`
        """
        cdef Row result = Row()
        result.thisptr[0] = row.queens(n)
        return result

    @staticmethod
    def kings(int n) -> Row:
        """
        Returns the row corresponding to kings on *n* bells.

        :param int n: number of bells
        :return: the computed row
        :rtype: :class:`Row`
        """
        cdef Row result = Row()
        result.thisptr[0] = row.kings(n)
        return result

    @staticmethod
    def tittums(int n) -> Row:
        """
        Returns the row corresponding to tittums on *n* bells.

        :param int n: number of bells
        :return: the computed row
        :rtype: :class:`Row`
        """
        cdef Row result = Row()
        result.thisptr[0] = row.tittums(n)
        return result

    @staticmethod
    def reverse_rounds(int n) -> Row:
        """
        Returns the row corresponding to reverse_rounds on *n* bells.

        :param int n: number of bells
        :return: the computed row
        :rtype: :class:`Row`
        """
        cdef Row result = Row()
        result.thisptr[0] = row.reverse_rounds(n)
        return result

    @staticmethod
    def cyclic(int n, int h=1, int c=1) -> Row:
        """
        Returns a cyclic row on *n* bells with *h* initial fixed (hunt) bells.
        The variable *c* controls the number of bells moved from the front of
        the row to the end:

        >>> from ringing import Row
        >>> Row.cyclic(6, 1, 2)
        Row('145623')

        :param int n: number of bells
        :param int h: number of hunt bells
        :param int c: number of bells to move to the end of the row
        :return: the computed row
        :rtype: :class:`Row`
        """
        cdef Row result = Row()
        result.thisptr[0] = row.cyclic(n, h, c)
        return result

    @staticmethod
    def pblh(int n, int h=1) -> Row:
        """
        Returns the first lead head of Plain Bob (*h* = 1), Grandsire
        (*h* = 2), or more generally the Plain Bob type method on *n* bells
        with *h* hunt bells:

        >>> from ringing import Row
        >>> Row.pblh(6)
        Row('135264')

        :param int n: number of bells
        :param int h: number of hunt bells
        :return: the computed row
        :rtype: :class:`Row`
        """
        cdef Row result = Row()
        result.thisptr[0] = row.pblh(n, h)
        return result

    def is_rounds(self) -> bool:
        """
        Determines whether the row is rounds:

        >>> from ringing import Row
        >>> Row('12345678').is_rounds()
        True
        >>> Row('72635184').is_rounds()
        False

        :return: ``True`` if the row is rounds, and ``False`` otherwise
        :rtype: boolean
        """
        return self.thisptr.isrounds()

    def is_pblh(self, int hunts=0) -> int:
        """
        If the row is a lead head of Plain Bob, Grandsire or, more generally,
        of the Plain Bob type method with any number of hunt bells, then this
        function returns an integer indicating which lead head it is.
        Otherwise, it returns ``False``.

        :param int hunts: number of hunt bells
        :return: lead head number, or ``False`` if not a Plain Bob-type lead head
        :rtype: int
        """
        if hunts:
            result = self.thisptr.ispblh(hunts)
        else:
            result = self.thisptr.ispblh()

        if result == 0:
            result = False

        return result

    def sign(self) -> Literal[+1, -1]:
        """
        Returns the sign or parity of a row:

        >>> from ringing import Row
        >>> Row('12345678').sign()
        1
        >>> Row('21345678').sign()
        -1

        :return: 1 for even, -1 for odd
        :rtype: int
        """
        return self.thisptr.sign()

    def cycles(self) -> str:
        """
        Expresses the row as separate cycles. The returned string will
        afterwards contain a list of all the cycles in the row, separated by
        commas:

        >>> from ringing import Row
        >>> Row('21453678').cycles()
        '12,345,6,7,8'

        :return: representation of the row as disjoint cycles
        :rtype: string
        """
        return self.thisptr.cycles().decode('ascii')

    def num_cycles(self) -> int:
        """
        Returns the number of cycles in the row:

        >>> from ringing import Row
        >>> Row('21453678').num_cycles()
        5

        :return: number of disjoint cycles in the row
        :rtype: int
        """
        return self.thisptr.num_cycles()

    def cycle_size(self, b: BellSpec) -> int:
        """
        Returns the size of the cycle containing bell *b*:

        >>> from ringing import Row
        >>> Row('21453678').cycle_size(0)
        2
        >>> Row('21453678').cycle_size('3')
        3

        :param bell b: bell to find
        :type b: :class:`Bell` or string or int
        :return: size of the cycle containing bell *b*
        :rtype: int
        :raises: ``ValueError`` if the bell is out of range
        """
        cdef bell bb = deref(Bell(b).thisptr)

        if <int>bb >= self.bells:
            raise ValueError('Bell too large for row')

        return self.thisptr.cycle_size(<int>bb)

    def order(self) -> int:
        """
        Returns the order of the row:

        >>> from ringing import Row
        >>> r = Row('21453678')
        >>> r.order()
        6
        >>> (r ** 6).is_rounds()
        True

        :return: the row's order
        :rtype: int
        """
        return self.thisptr.order()

    def find(self, b: BellSpec) -> int:
        """
        Locates the bell, *b*, in this row and returns its place:

        >>> from ringing import Row
        >>> r = Row('512364')
        >>> r.find(0)
        1
        >>> r.find('2')
        2

        See also :meth:`__getitem__`.

        :param b: bell to find
        :type b: :class:`Bell` or string or int
        :return: bell position (0-indexed)
        :rtype: int
        """
        cdef bell bb = deref(Bell(b).thisptr)
        return self.thisptr.find(bb)

    @staticmethod
    def conjugator(x: RowSpec, y: RowSpec) -> Row:
        """
        Two rows, *x* and *y*, are conjugate if there exists some row, *r*,
        such that::

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
        """
        cdef Row result = Row()
        result.thisptr[0] = conjugator(
            deref(Row(x).thisptr),
            deref(Row(y).thisptr),
        )
        if result == Row():
            return None
        else:
            return result

    @staticmethod
    def are_conjugate(x: RowSpec, y: RowSpec) -> bool:
        """
        Determines whether the rows *x* and *y* are conjugate as described
        above.

        :param x: row ``x``
        :type x: :class:`Row` or int or string
        :param y: row ``y``
        :type y: :class:`Row` or int or string
        :return: ``True`` if the rows are conjugate, or ``False`` otherwise
        :rtype: boolean
        """
        return are_conjugate(deref(Row(x).thisptr), deref(Row(y).thisptr))

    def __richcmp__(self, other, int op) -> bool:
        cdef row rx
        cdef row ry

        rx = deref((<Row>self).thisptr)

        try:
            ry = deref(Row(other).thisptr)
        except TypeError:
            return NotImplemented

        if op == 0:  # <
            return rx < ry
        elif op == 1:  # <=
            return rx <= ry
        elif op == 2:  # ==
            return rx == ry
        elif op == 3:  # !=
            return rx != ry
        elif op == 4:  # >
            return rx > ry
        elif op == 5:  # >=
            return rx >= ry

    def __str__(self) -> str:
        return self.thisptr.print().decode('ascii')

    def __bytes__(self) -> bytes:
        return self.thisptr.print()

    def __repr__(self) -> str:
        if self.thisptr.bells():
            return f"Row('{self}')"
        else:
            return 'Row()'

    def __hash__(self) -> int:
        return self.thisptr.hash()

    def __mul__(self, other) -> Row:
        """
        Multiples two rows together **or** applies a change to a row.

        A row multiplied by a change returns the effect of applying that change
        to the row:

        >>> from ringing import Row, Change
        >>> Row('214365') * Change(6, '1')
        Row('241635')

        .. note::
            If the number of bells *c* differs from the number of bells in
            *r*\ , then *c* is considered to be padded or truncated in the
            obvious way.

        A row can be multiplied by another as explained above:

        >>> from ringing import Row
        >>> r = Row('21345678')
        >>> r * '13572468'
        Row('23571468')
        >>> '13572468' * r
        Row('31572468')

        .. note::
            If the rows are not of the same length, the shorter row is
            considered to be first padded out to the length of the longer row
            by adding the extra bells in order at the end.

        :param input: value to multiply by
        :type input: :class:`Change` or :class:`Row` or int or string
        :return: result
        :rtype: :class:`Row`
        """
        cdef Row result = Row()

        try:
            if isinstance(other, Change):
                result.thisptr[0] = deref((<Row>self).thisptr) * \
                                    deref((<Change>other).thisptr)
            else:
                result.thisptr[0] = deref((<Row>self).thisptr) * \
                                    deref(Row(other).thisptr)
        except TypeError:
            return NotImplemented
        else:
            return result

    def __rmul__(self, other) -> Row:
        cdef Row result = Row()

        try:
            result.thisptr[0] = deref(Row(other).thisptr) * \
                deref((<Row>self).thisptr)
        except TypeError:
            return NotImplemented
        else:
            return result

    def __truediv__(self, other) -> Row:
        """
        Divides two rows, as explained above:

        >>> from ringing import Row
        >>> Row('23571468') / Row('13572468')
        Row('21345678')

        .. note::
            If the rows are not of the same length, the shorter row is
            considered to be first padded out to the length of the longer row
            by adding the extra bells in order at the end.

        :param row: value to divide by
        :type row: :class:`Row` or int or string
        :return: result
        :rtype: :class:`Row`
        """
        cdef Row result = Row()

        try:
            result.thisptr[0] = deref((<Row>self).thisptr) / \
                deref(Row(other).thisptr)
        except TypeError:
            return NotImplemented
        else:
            return result

    def __rtruediv__(self, other) -> Row:
        cdef Row result = Row()

        try:
            result.thisptr[0] = deref(Row(other).thisptr) / \
                deref((<Row>self).thisptr)
        except TypeError:
            return NotImplemented
        else:
            return result

    def __pow__(Row x, int y, z) -> Row:
        """
        Returns the *n*\ th power of a row:

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
        """
        cdef Row result = Row()
        result.thisptr[0] = Row(x).thisptr.power(y)
        return result

    def __invert__(self) -> Row:
        """
        Returns the inverse of a row:

        >>> from ringing import Row
        >>> r = Row('13572468')
        >>> ~r
        Row('15263748')
        >>> r * ~r
        Row('12345678')
        >>> ~r * r
        Row('12345678')

        :return: the row's inverse
        :rtype: :class:`Row`
        """
        return self.inverse()

    def __len__(self) -> int:
        return self.bells

    def __getitem__(self, int x) -> Bell:
        """
        This returns the *i*\ th bell in the row:

        >>> from ringing import Row
        >>> r = Row('512364')
        >>> r[0]
        Bell(4)
        >>> r[1].to_char()
        '1'
        >>> print([b for b in r])
        [Bell(4), Bell(0), Bell(1), Bell(2), Bell(5), Bell(3)]

        .. note::

            Note that this is not an lvalue,
            so you cannot assign a value to an individual bell in a row.

        :param int i: bell position to return (0-indexed)
        :return: bell number in that position (0-indexed; ``0`` is the treble)
        :rtype: :class:`Bell`
        """
        if 0 <= x < self.bells:
            return Bell(<int>(deref(self.thisptr)[x]))
        else:
            raise IndexError('ringing.Row index out of range')
