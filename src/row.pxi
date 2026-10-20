from typing import Literal, TypeAlias


RowSpec: TypeAlias = Row | int | str | bytes | None


cdef class Row:

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
        cdef Row result = Row()
        result.thisptr[0] = self.thisptr.inverse()
        return result

    property bells:
        def __get__(self) -> int:
            return self.thisptr.bells()

    def conjugate(self, r: RowSpec) -> Row:
        cdef Row result = Row()
        result.thisptr[0] = self.thisptr.conjugate(deref(Row(r).thisptr))
        return result

    @staticmethod
    def rounds(int n) -> Row:
        cdef Row result = Row()
        result.thisptr[0] = row.rounds(n)
        return result

    @staticmethod
    def queens(int n) -> Row:
        cdef Row result = Row()
        result.thisptr[0] = row.queens(n)
        return result

    @staticmethod
    def kings(int n) -> Row:
        cdef Row result = Row()
        result.thisptr[0] = row.kings(n)
        return result

    @staticmethod
    def tittums(int n) -> Row:
        cdef Row result = Row()
        result.thisptr[0] = row.tittums(n)
        return result

    @staticmethod
    def reverse_rounds(int n) -> Row:
        cdef Row result = Row()
        result.thisptr[0] = row.reverse_rounds(n)
        return result

    @staticmethod
    def cyclic(int n, int h=1, int c=1) -> Row:
        cdef Row result = Row()
        result.thisptr[0] = row.cyclic(n, h, c)
        return result

    @staticmethod
    def pblh(int n, int h=1) -> Row:
        cdef Row result = Row()
        result.thisptr[0] = row.pblh(n, h)
        return result

    def is_rounds(self) -> bool:
        return self.thisptr.isrounds()

    def is_pblh(self, int hunts=0) -> int:
        if hunts:
            result = self.thisptr.ispblh(hunts)
        else:
            result = self.thisptr.ispblh()

        if result == 0:
            result = False

        return result

    def sign(self) -> Literal[+1, -1]:
        return self.thisptr.sign()

    def cycles(self) -> str:
        return self.thisptr.cycles().decode('ascii')

    def num_cycles(self) -> int:
        return self.thisptr.num_cycles()

    def cycle_size(self, b: BellSpec) -> int:
        cdef bell bb = deref(Bell(b).thisptr)

        if <int>bb >= self.bells:
            raise ValueError('Bell too large for row')

        return self.thisptr.cycle_size(<int>bb)

    def order(self) -> int:
        return self.thisptr.order()

    def find(self, b: BellSpec) -> int:
        cdef bell bb = deref(Bell(b).thisptr)
        return self.thisptr.find(bb)

    @staticmethod
    def conjugator(x: RowSpec, y: RowSpec) -> Row:
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
        cdef Row result = Row()
        result.thisptr[0] = Row(x).thisptr.power(y)
        return result

    def __invert__(self) -> Row:
        return self.inverse()

    def __len__(self) -> int:
        return self.bells

    def __getitem__(self, int x) -> Bell:
        if 0 <= x < self.bells:
            return Bell(<int>(deref(self.thisptr)[x]))
        else:
            raise IndexError('ringing.Row index out of range')
