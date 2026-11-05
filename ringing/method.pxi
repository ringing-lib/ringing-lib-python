from typing import TypeAlias


MethodSpec: TypeAlias = Method | int | str | bytes | None


cdef class Method:
    """
    Constructs a Method.

    Methods may be constructed in a variety of ways:

    >>> from ringing import Method
    >>> Method(2, 4)  # from an integer length
    Method('1234.1234', 4, 'Untitled')
    >>> Method('&-1-1,2', 4)  # from a place notation
    Method('&-14-14,12', 4, 'Untitled')
    >>> Method(Method())  # from another method
    Method('', 0, 'Untitled')

    .. note::

        The number of bells defaults to zero.
        If unspecified, any string of place notation will be decomposed into
        zero-bell changes, with :exc:`ValueError` exceptions raised for any
        out-of-range notations.
        Always specify the number of bells!

    A method behaves much like a list of :class:`Change` objects, and supports
    the following sequence operations:

    ===============  ==========================================================
    Operation        Result
    ===============  ==========================================================
    ``c in m``       ``True`` if an item of *m* is equal to *c*, else ``False``
    ``c not in m``   ``False`` if an item of *m* is equal to *c*, else ``True``
    ``m[i]``         *i*\ th change of *m* (0-indexed)
    ``m[i] = c``     sets *i*\ th change of *m*
    ``len(m)``       length (:attr:`size`) of *m*
    ``list(m)``      list of changes in *m*
    ``m.append(c)``  appends *c* to the end of the method
    ===============  ==========================================================

    The syntax of the place notation is as follows: place notation consists of
    a sequence of blocks, which are delimited by commas. Each block is a
    sequence of changes, with ``X`` or ``-`` meaning a cross change. Changes
    other than cross changes are separated by full stops. A block may
    optionally be preceded by an ampersand ``&``, which means that the entire
    block, except the last change, is repeated backwards. All other characters
    are ignored.

    :param input: Specification for constructing the method.
        This might be:

        * Nothing. Constructs a zero-length method.
        * Another method. Constructs a copy.
        * An integer length. Constructs a method of the specified length.
        * A string (``str`` or ``bytes``) place notation.
    :type input: :class:`Method` or int or string
    :param int bells: number of bells
    :param string name: base name of the method
    """

    cdef method *thisptr

    def __cinit__(
        self,
        input: MethodSpec = None,
        int bells = 0,
        name: str | bytes = 'Untitled',
    ):
        cdef string name_string

        # Validate bells parameter
        if not (0 <= bells <= MAX_BELL_NUMBER):
            raise ValueError('Number of bells out of range')

        # Process name parameter
        if isinstance(name, str):
            name_string = <string>(name.encode())
        elif isinstance(name, bytes):
            name_string = <string>name
        else:
            raise TypeError("Cannot convert {type} to str".format(
                type=type(name).__name__
            ))

        if input is None:
            self.thisptr = new method()
        elif isinstance(input, Method):
            self.thisptr = new method(deref((<Method>input).thisptr))
        elif isinstance(input, int):
            if 0 <= input:
                self.thisptr = new method(
                    <int>input,
                    bells,
                    name_string.c_str(),
                )
            else:
                raise ValueError('Length of method must be greater than 0')
        elif isinstance(input, str):
            self.thisptr = new method(
                <string>(input.encode('ascii')),
                bells,
                name_string,
            )
        elif isinstance(input, bytes):
            self.thisptr = new method(<string>input, bells, name_string)
        else:
            raise TypeError('Cannot convert {type} to ringing.Method'.format(
                type=type(input).__name__,
            ))

    def __dealloc__(self):
        del self.thisptr

    @property
    def name(self) -> str:
        """
        Base name of the method. Note that this may be an empty string, for
        example in Little Bob.
        Unlike many attributes in this library, a new value may be assigned to
        this attribute:

        >>> from ringing import Method
        >>> m = Method('&-1-1-1,2', 6)
        >>> m.name
        'Untitled'
        >>> m.name = 'Plain'
        >>> m
        Method('&-16-16-16,12', 6, 'Plain')

        """
        return (<bytes>self.thisptr.name()).decode()

    @name.setter
    def name(self, value: str | bytes) -> None:
        if isinstance(value, str):
            self.thisptr.name(<string>(value.encode()))
        elif isinstance(value, bytes):
            self.thisptr.name(<string>value)
        else:
            raise TypeError('Cannot convert {type} to string'.format(
                type=type(input).__name__,
            ))

    def full_name(self) -> str:
        """
        Assembles the full name of the method:

        >>> from ringing import Method
        >>> Method('&-1-1-1,2', 6, 'Plain').full_name()
        'Plain Bob Minor'

        The full name consists of:
        * the base name of the method;
        * the word "Little", if appropriate;
        * the class of the method, or none if it is a principle;
        * the stage (number of bells) of the method

        Note that Grandsire, Union and their related methods are treated
        specially: the full name of these methods does not include their class,
        nor in the case of Little Grandsire does it contain "Little".

        :return: full name
        :rtype: string
        """
        return (<bytes>self.thisptr.fullname()).decode()

    @staticmethod
    def stage_name(int bells) -> str:
        """
        Returns a string describing the stage of *bells* bells: thus
        "``Minimus``", "``Doubles``", and so on:

        >>> from ringing import Method
        >>> Method.stage_name(8)
        'Major'

        For stages above Sixteen, the number is given in digits.

        :param int bells: number of bells
        :return: stage name
        :rtype: string
        """
        if 0 <= bells <= MAX_BELL_NUMBER:
            return (<bytes>method.stagename(bells)).decode('ascii')
        else:
            raise ValueError('Number of bells out of range')

    @property
    def size(self) -> int:
        """
        Number of changes in a lead of the method:

        >>> from ringing import Method
        >>> Method('&-1-1-1,2', 6).size
        12

        You may prefer to use the ``len()`` of the method.
        """
        return self.thisptr.size()

    @property
    def length(self) -> int:
        """
        Synonym for :attr:`size`.
        """
        return self.thisptr.length()

    @property
    def bells(self) -> int:
        """
        Number of bells on which the method is defined:

        >>> from ringing import Method
        >>> Method('&-1-1-1,2', 6).bells
        6

        """
        return self.thisptr.bells()

    def lead_head(self) -> Row:
        """
        Returns the first lead head of the method:

        >>> from ringing import Method
        >>> Method('&-1-1-1,2', 6).lead_head()
        Row('135264')

        :return: first lead head
        :rtype: :class:`Row`
        """
        cdef Row result = Row()
        result.thisptr[0] = self.thisptr.lh()
        return result

    def is_symmetric(self, b: BellSpec = None) -> bool:
        """
        Returns ``True`` if the method is symmetrical about the half lead (and
        has an even number of changes in the lead), or ``False`` otherwise.
        If a *bell* number is specified, returns ``True`` if the path of that
        bell in a lead of the method is symmetrical about the half lead, or
        ``False`` otherwise.

        :param bell: bell to check
        :type bell: :class:`Bell` or string or int
        :return: whether the method is symmetric
        :rtype: boolean
        """
        cdef bell bb

        if b is None:
            return self.thisptr.issym()
        else:
            bb = deref(Bell(b).thisptr)
            if <int>bb < self.bells:
                return self.thisptr.issym(bb)
            else:
                raise IndexError('Bell number out of range')

    def is_palindromic(self, b: BellSpec = None) -> bool:
        """
        Returns ``True`` if the method is symmetrical about any point (and has
        an even number of changes in the lead), or ``False`` otherwise.
        If a *bell* number is specified, returns ``True`` if the path of that
        bell in a lead of the method is symmetrical about any point, or
        ``False`` otherwise.

        :param bell: bell to check
        :type bell: :class:`Bell` or string or int
        :return: whether the method is symmetric
        :rtype: boolean
        """
        cdef bell bb

        if self.size % 2:
            raise ValueError('Method contains an odd number of changes')

        if b is None:
            return self.thisptr.ispalindromic()
        else:
            bb = deref(Bell(b).thisptr)
            if <int>bb < self.bells:
                return self.thisptr.ispalindromic(bb)
            else:
                raise IndexError('Bell number out of range')

    def is_double(self) -> bool:
        """
        Returns ``True`` if the method is double, or ``False`` otherwise. Note
        that double does not imply symmetrical.

        :return: whether the method is double
        :rtype: boolean
        """
        return self.thisptr.isdouble()

    def is_regular(self) -> bool:
        """
        Returns ``True`` if the method is regular (that is, it has Plain Bob
        lead heads), or ``False`` otherwise.

        :return: whether the method is regular
        :rtype: boolean
        """
        return self.thisptr.isregular()

    def hunt_bells(self) -> int:
        """
        Returns the number of hunt bells in the method:

        >>> from ringing import Method
        >>> Method('&-1-1-1,2', 6).hunt_bells()
        1

        :return: number of hunt bells
        :rtype: int
        """
        return self.thisptr.huntbells()

    def leads(self) -> int:
        """
        Returns the number of leads in the plain course of the method.
        This is equivalent to the order of the lead-head row:

        >>> from ringing import Method
        >>> Method('&-1-1-1,2', 6).leads()
        5
        >>> Method('&-1-1-1,2', 6).lead_head().order()
        5

        :return: number of leads
        :rtype: int
        """
        return self.thisptr.leads()

    def is_plain(self, b: BellSpec = 0) -> bool:
        """
        Returns ``True`` if *bell* plain hunts for the whole lead of the
        method, or ``False`` otherwise.

        If *bell* is not provided then the treble path is checked.

        :param bell: bell to check
        :type bell: :class:`Bell` or string or int
        :return: whether the bell plain hunts
        :rtype: boolean
        """
        cdef bell bb = deref(Bell(b).thisptr)

        if <int>bb < self.bells:
            return self.thisptr.isplain(bb)
        else:
            raise IndexError('Bell number out of range')

    def has_dodges(self, b: BellSpec) -> bool:
        """
        Returns ``True`` if *bell* dodges during the lead, or ``False``
        otherwise.

        :param bell: bell to check
        :type bell: :class:`Bell` or string or int
        :return: whether the bell dodges
        :rtype: boolean
        """
        cdef bell bb = deref(Bell(b).thisptr)

        if <int>bb < self.bells:
            return self.thisptr.hasdodges(bb)
        else:
            raise IndexError('Bell number out of range')

    def has_places(self, b: BellSpec) -> bool:
        """
        Returns ``True`` if *bell* makes any internal places during the lead,
        or ``False`` otherwise.

        :param bell: bell to check
        :type bell: :class:`Bell` or string or int
        :return: whether the bell makes internal places
        :rtype: boolean
        """
        cdef bell bb = deref(Bell(b).thisptr)

        if <int>bb < self.bells:
            return self.thisptr.hasplaces(bb)
        else:
            raise IndexError('Bell number out of range')

    def lh_code(self) -> str:
        """
        Returns the standard code for the lead end and lead head of the
        method:

        >>> from ringing import Method
        >>> Method('&-1-1-1,2', 6).lh_code()
        'a'

        :return: lead head code
        :rtype: string
        """
        return (<bytes>self.thisptr.lhcode()).decode('ascii')

    def symmetry_point(self, b: BellSpec = None) -> int:
        cdef bell bb
        cdef int result

        if self.size % 2:
            raise ValueError('Method contains an odd number of changes')

        if b is None:
            result = self.thisptr.symmetry_point()
        else:
            bb = deref(Bell(b).thisptr)
            if <int>bb < self.bells:
                result = self.thisptr.symmetry_point(bb)
            else:
                raise IndexError('Bell number out of range')

        if result == -1:
            return False

        return result

    def max_blows(self) -> int:
        """
        Returns the maximum consecutive blows made in any place in this method.
        (If the method has one bell fixed throughout, the lead length is
        returned.):

        >>> from ringing import Method
        >>> Method('&-1-1-1,2', 6).max_blows()
        2

        :return: maximum consecutive blows
        :rtype: int
        """
        return self.thisptr.maxblows()

    def format(self, **kwargs) -> str:
        """
        Formats the method's place notation into a string:

        >>> from ringing import Method
        >>> Method('&-1-1-1,2', 6).format(
        ...     all_dots=True,
        ...     external_places=True,
        ...     cross_lower_x=True,
        ... )
        'x.16.x.16.x.16.x.16.x.16.x.12'

        Set keyword arguments listed below to ``True`` to control the format.

        .. warning::
            Some arguments conflict with each other (e.g. ``cross_upper_x`` and
            ``cross_lower_x``); if used together then the result is undefined.

        .. warning::
            The ``symmetry`` and ``full_symmetry`` options may not be used for
            methods that have an odd number of changes. This is a constraint of
            the underlying library.

        :param boolean all_dots: include all dots
        :param boolean external_places: include all external places
        :param boolean cross_upper_x: use an '``X``' for the cross change
        :param boolean cross_lower_x: use an '``x``' for the cross change
        :param boolean cross_dash: use a '``-``' for the cross change
        :param boolean symmetry: split palindromic methods into two components
        :param boolean full_symmetry: as above but with other symmetry points
        :param boolean omit_lh: omit the lead head change
        :param boolean asymmetric_plus: prefix asymmetric sections with '``+``'
        :return: formatted place notation
        :rtype: string
        :raises: :exc:`ValueError` for symmetry flags with an odd-length method
        """
        cdef int format = 0
        parameter_mapping = {
            'all_dots': 0o1,
            'external_places': 0o2,
            'cross_upper_x': 0o4,
            'cross_lower_x': 0o10,
            'cross_dash': 0o20,
            'symmetry': 0o40,
            'full_symmetry': 0o140,
            'omit_lh': 0o200,
            'asymmetric_plus': 0o400,
        }
        for key, value in parameter_mapping.items():
            if kwargs.get(key, False):
                format |= value

        if self.size % 2 and format & 0o40:
            raise ValueError(
                'Cannot use symmetry flags with methods '
                'containing an odd number of changes',
            )

        return (<bytes>self.thisptr.format(format)).decode('ascii')

    def append(self, c: Change | str | bytes) -> None:
        """
        Adds a change to the end of the method. The *change* may be provided as
        a :class:`Change` object or a string containing the place notation to
        be added.

        :param change: change to be added
        :type change: :class:`Change` or string
        """
        if isinstance(c, Change):
            self.thisptr.push_back(deref((<Change>c).thisptr))
        elif isinstance(c, str):
            self.thisptr.push_back(<string>(c.encode('ascii')))
        elif isinstance(c, bytes):
            self.thisptr.push_back(<string>c)
        else:
            raise TypeError("Cannot append {type} to ringing.Method".format(
                type=type(c).__name__,
            ))

    def __richcmp__(self, other, int op) -> bool:
        cdef method mx
        cdef method my

        mx = deref((<Method>self).thisptr)

        try:
            my = deref(Method(other).thisptr)
        except TypeError:
            return NotImplemented

        if op == 0:  # <
            return mx < my
        elif op == 1:  # <=
            return mx <= my
        elif op == 2:  # ==
            return mx == my
        elif op == 3:  # !=
            return mx != my
        elif op == 4:  # >
            return mx > my
        elif op == 5:  # >=
            return mx >= my

    def __str__(self) -> str:
        return (<bytes>self.thisptr.fullname()).decode()

    def __bytes__(self) -> bytes:
        return <bytes>self.thisptr.fullname()

    def __repr__(self) -> str:
        format = {'external_places': True, 'cross_dash': True}
        if self.size % 2:
            format['asymmetric_plus'] = True
        else:
            format['symmetry'] = True

        return "Method('{pn}', {bells}, '{name}')".format(
            pn=self.format(**format),
            bells=self.bells,
            name=self.name,
        )

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, int x) -> Change:
        cdef Change result = Change()

        if 0 <= x < self.size:
            result.thisptr[0] = deref(self.thisptr)[x]
            return result
        else:
            raise IndexError('ringing.Method index out of range')

    def __setitem__(self, int x, y: ChangeSpec) -> None:
        cdef Change cy = Change(y)

        if 0 <= x < self.size:
            deref(self.thisptr)[x] = deref(cy.thisptr)
        else:
            raise IndexError('ringing.Method index out of range')
