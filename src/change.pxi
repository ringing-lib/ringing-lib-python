cdef class Change:

    cdef change *thisptr

    def __cinit__(self, input=None, change_str=None):
        if input is None:
            self.thisptr = new change()
        elif isinstance(input, Change):
            self.thisptr = new change(deref((<Change>input).thisptr))
        elif isinstance(input, int):
            if 0 <= input <= 256:
                if change_str is None:
                    self.thisptr = new change(<int>input)
                elif isinstance(change_str, unicode):
                    self.thisptr = new change(<int>input,
                                              <string>(change_str.encode()))
                elif isinstance(change_str, bytes):
                    self.thisptr = new change(<int>input, <string>change_str)
                else:
                    raise TypeError('supplied change must be a string')
            else:
                raise ValueError('number of bells must be between 0 and 256')
        else:
            raise TypeError

    def __dealloc__(self):
        del self.thisptr

    property bells:
        def __get__(self):
            return self.thisptr.bells()

    def __richcmp__(x, y, int op):
        cdef Change cx
        cdef Change cy

        if isinstance(x, Change):
            cx = Change(x)
        elif isinstance(x, bytes) or isinstance(x, unicode):
            cx = Change(y.bells, x)
        else:
            return NotImplemented

        if isinstance(y, Change):
            cy = Change(y)
        elif isinstance(y, bytes) or isinstance(y, unicode):
            cy = Change(x.bells, y)
        else:
            return NotImplemented

        if op == 0:  # <
            return deref(cx.thisptr) < deref(cy.thisptr)
        elif op == 1:  # <=
            return deref(cx.thisptr) <= deref(cy.thisptr)
        elif op == 2:  # ==
            return deref(cx.thisptr) == deref(cy.thisptr)
        elif op == 3:  # !=
            return deref(cx.thisptr) != deref(cy.thisptr)
        elif op == 4:  # >
            return deref(cx.thisptr) > deref(cy.thisptr)
        elif op == 5:  # >=
            return deref(cx.thisptr) >= deref(cy.thisptr)

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
            return 'Change({bells}, "{change}")'.format(
                bells = self.thisptr.bells(),
                change = self.__str__(),
            )
        else:
            return 'Change()'
