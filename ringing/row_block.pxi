from collections.abc import Iterable


cdef class RowBlock:
    """
    Creates a block of rows using the changes in *changes*, starting from the
    row given in *starting_row* (or rounds if *starting_row* is not provided).

    Row blocks support several standard sequence operations:

    >>> from ringing import RowBlock, Change
    >>> rb = RowBlock([Change(5, '3'), Change(5, '1'), Change(5, '5')])
    >>> rb[0]
    Row('12345')
    >>> for r in rb:
    ...     print(r)
    ...
    12345
    21354
    23145
    32415

    ========================  =================================================
    Operation                 Result
    ========================  =================================================
    ``r in rb``               ``True`` if an item of *rb* is equal to *r*,
                              else ``False``
    ``r not in rb``           ``False`` if an item of *rb* is equal to *r*,
                              else ``True``
    ``rb[i]``                 *i*\ th row of *rb* (0-indexed)
    ``rb[i] = Row('12345')``  sets *i*\ th row of *rb*
    ``len(rb)``               length (:attr:`size`) of *rb*
    ``list(rb)``              list of rows in *rb*
    ========================  =================================================

    :param changes: changes to associate with the block
    :type changes: [:class:`Change`] or :class:`Method`
    :param starting_row: optional starting row
    :type starting_row: :class:`Row`
    """

    cdef row_block *thisptr

    cdef vector[change] change_vector

    cdef change_list

    def __cinit__(
        self,
        changes: Iterable[Change],
        starting_row: RowSpec = None,
    ):
        cdef row starting_row_obj = deref(Row(starting_row).thisptr)

        self.change_list = []
        for ch in changes:
            self.change_vector.push_back(deref((<Change?>ch).thisptr))
            self.change_list.append(ch)

        if starting_row is None:
            self.thisptr = new row_block(self.change_vector)
        else:
            self.thisptr = new row_block(self.change_vector, starting_row_obj)

    def __dealloc__(self):
        del self.thisptr

    @property
    def size(self) -> int:
        """
        Number of rows which the row block contains:

        >>> from ringing import RowBlock, Change
        >>> rb = RowBlock([Change(5, '3'), Change(5, '1'), Change(5, '5')])
        >>> rb.size
        4

        You may prefer to use the ``len()`` of the row block.
        """
        return self.thisptr.size()

    @property
    def changes(self) -> list[Change]:
        """
        List of changes associated with the row block:

        >>> from ringing import RowBlock, Change
        >>> rb = RowBlock([Change(5, '3'), Change(5, '1'), Change(5, '5')])
        >>> rb.changes
        [Change(5, '3'), Change(5, '1'), Change(5, '5')]

        It's also possible to assign a new set of changes:

        >>> from ringing import RowBlock, Change
        >>> rb = RowBlock([Change(5, '3'), Change(5, '1'), Change(5, '5')])
        >>> list(rb)
        [Row('12345'), Row('21354'), Row('23145'), Row('32415')]
        >>> rb.changes = [Change(5, pn) for pn in ['5', '3']]
        >>> list(rb)
        [Row('12345'), Row('21435'), Row('12453')]
        """
        return self.change_list[:]

    @changes.setter
    def changes(self, value: Iterable[Change]) -> None:
        cdef row_block *our_rb_ptr = self.thisptr

        # Create a new RowBlock (may raise exceptions)...
        cdef RowBlock new_row_block = RowBlock(value, self[0])

        # ... suck its brains out...
        self.thisptr = new_row_block.thisptr
        self.change_vector = new_row_block.change_vector
        self.change_list = new_row_block.change_list

        # ... and put our thisptr into it so it gets deallocated
        new_row_block.thisptr = our_rb_ptr

    def set_start(self, starting_row: RowSpec) -> None:
        """
        Assigns a new row for the start of the row block.
        Other rows remain unmodified; call :meth:`recalculate` to update them:

        >>> from ringing import RowBlock, Change
        >>> rb = RowBlock([Change(5, '3'), Change(5, '1'), Change(5, '5')])
        >>> list(rb)
        [Row('12345'), Row('21354'), Row('23145'), Row('32415')]
        >>> rb.set_start('54321')
        >>> list(rb)
        [Row('54321'), Row('21354'), Row('23145'), Row('32415')]
        >>> rb.recalculate()
        >>> list(rb)
        [Row('54321'), Row('45312'), Row('43521'), Row('34251')]

        :param starting_row: new starting row
        :type starting_row: :class:`Row` or int or string
        :return: ``None``
        """
        cdef Row starting_row_obj = Row(starting_row)
        self.thisptr.set_start(deref(starting_row_obj.thisptr))

    def recalculate(self, int start=0) -> None:
        """
        Recalculates the rows within the row block:

        >>> from ringing import RowBlock, Change
        >>> rb = RowBlock([Change(5, '3'), Change(5, '1'), Change(5, '5')])
        >>> list(rb)
        [Row('12345'), Row('21354'), Row('23145'), Row('32415')]
        >>> rb[2] = '54321'
        >>> list(rb)
        [Row('12345'), Row('21354'), Row('54321'), Row('32415')]
        >>> rb.recalculate(2)
        >>> list(rb)
        [Row('12345'), Row('21354'), Row('54321'), Row('45231')]

        :param int start: if supplied, only rows after this index will be
            recalculated
        :return: ``None``
        :raises: :exc:`IndexError` if ``start`` is out of range
        """
        if 0 <= start < self.size:
            self.thisptr.recalculate(start)
        else:
            raise IndexError('ringing.RowBlock index out of range')

    def __repr__(self) -> str:
        cdef str changes = ', '.join([repr(ch) for ch in self.change_list])
        if self[0].is_rounds():
            return f'RowBlock([{changes}])'
        else:
            return f'RowBlock([{changes}], {repr(self[0])})'

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, int x) -> Row:
        cdef Row result = Row()

        if 0 <= x < self.size:
            result.thisptr[0] = deref(self.thisptr)[x]
            return result
        else:
            raise IndexError('ringing.RowBlock index out of range')

    def __setitem__(self, int x, y: RowSpec) -> None:
        cdef Row ry = Row(y)

        if 0 <= x < self.size:
            deref(self.thisptr)[x] = deref(ry.thisptr)
        else:
            raise IndexError('ringing.RowBlock index out of range')
