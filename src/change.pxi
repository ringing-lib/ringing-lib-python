cdef class Change:

    cdef change *thisptr

    def __cinit__(self, input=None, change_str=None):
        if input is None:
            self.thisptr = new change()
        elif isinstance(input, Change):
            self.thisptr = new change(deref((<Change>input).thisptr))
        elif isinstance(input, int):
            if 0 <= input <= MAX_BELL_NUMBER:
                if change_str is None:
                    self.thisptr = new change(<int>input)
                elif isinstance(change_str, unicode):
                    self.thisptr = new change(<int>input,
                                              <string>(change_str.encode()))
                elif isinstance(change_str, bytes):
                    self.thisptr = new change(<int>input, <string>change_str)
                else:
                    raise TypeError('Cannot convert {type} to str'.format(
                        type=type(change_str).__name__
                    ))
            else:
                raise ValueError('Number of bells out of range')
        else:
            raise TypeError('Cannot convert {type} to ringing.Change'.format(
                type=type(input).__name__
            ))

    def __dealloc__(self):
        del self.thisptr

    def set(self, int num, pn):
        if 0 <= num <= MAX_BELL_NUMBER:
            if isinstance(pn, bytes):
                self.thisptr.set(num, pn)
            elif isinstance(pn, unicode):
                self.thisptr.set(num, pn.encode())
            else:
                raise TypeError('Cannot convert {type} to str'.format(
                    type=type(pn).__name__
                ))
        else:
            raise ValueError('Number of bells out of range')

    def reverse(self):
        cdef Change result = Change()
        result.thisptr[0] = self.thisptr.reverse()
        return result

    property bells:
        def __get__(self):
            return self.thisptr.bells()

    def sign(self):
        return self.thisptr.sign()

    def find_swap(self, b):
        cdef bell bb = deref(Bell(b).thisptr)
        if <int>bb < (self.thisptr.bells() - 1):
            return self.thisptr.findswap(bb)
        else:
            raise IndexError('ringing.Change index out of range')

    def find_place(self, b):
        cdef bell bb = deref(Bell(b).thisptr)
        if <int>bb <= (self.thisptr.bells() - 1):
            return self.thisptr.findplace(bb)
        else:
            raise IndexError('ringing.Change index out of range')

    def swap_pair(self, b):
        cdef bell bb = deref(Bell(b).thisptr)
        return self.thisptr.swappair(bb)

    def internal(self):
        return self.thisptr.internal()

    def count_places(self):
        return self.thisptr.count_places()

    def __richcmp__(self, other, int op):
        cdef change cx
        cdef change cy

        cx = deref((<Change>self).thisptr)

        if isinstance(other, Change):
            cy = deref(Change(other).thisptr)
        elif isinstance(other, bytes) or isinstance(other, unicode):
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

    def __str__(self):
        if PY_MAJOR_VERSION < 3:
            return self.__bytes__()
        else:
            return self.__unicode__()

    def __bytes__(self):
        return self.thisptr.print()

    def __unicode__(self):
        return self.thisptr.print().decode()

    def __repr__(self):
        if self.thisptr.bells():
            return "Change({bells}, '{change}')".format(
                bells = self.thisptr.bells(),
                change = self.__str__(),
            )
        else:
            return 'Change()'

    def __mul__(self, other):
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

    def __rmul__(self, other):
        return Change.__mul__(self, other)
