cdef class Method:

    cdef method *thisptr

    def __cinit__(self, input=None, int bells=0, name='Untitled'):
        cdef string name_string

        # Validate bells parameter
        if not (0 <= bells <= MAX_BELL_NUMBER):
            raise ValueError('Number of bells out of range')

        # Process name parameter
        if isinstance(name, unicode):
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
                self.thisptr = new method(<int>input, bells,
                                          name_string.c_str())
            else:
                raise ValueError('Length of method must be greater than 0')
        elif isinstance(input, unicode):
            self.thisptr = new method(<string>(input.encode()), bells,
                                      name_string)
        elif isinstance(input, bytes):
            self.thisptr = new method(<string>input, bells, name_string)
        else:
            raise TypeError('Cannot convert {type} to ringing.Method'.format(
                type=type(input).__name__
            ))

    def __dealloc__(self):
        del self.thisptr

    property size:
        def __get__(self):
            return self.thisptr.size()

    property length:
        def __get__(self):
            return self.thisptr.length()

    property bells:
        def __get__(self):
            return self.thisptr.bells()

    def lead_head(self):
        cdef Row result = Row()
        result.thisptr[0] = self.thisptr.lh()
        return result

    def is_sym(self, b=None):
        if b is None:
            return self.thisptr.issym()
        else:
            return self.thisptr.issym(bell(b))

    def is_palindromic(self, b=None):
        if b is None:
            return self.thisptr.ispalindromic()
        else:
            return self.thisptr.ispalindromic(bell(b))

    def is_double(self):
        return self.thisptr.isdouble()

    def is_regular(self):
        return self.thisptr.isregular()

    def hunt_bells(self):
        return self.thisptr.huntbells()

    def leads(self):
        return self.thisptr.leads()

    def is_plain(self, b=None):
        if b is None:
            return self.thisptr.isplain()
        else:
            return self.thisptr.isplain(bell(b))

    def has_dodges(self, int b):
        return self.thisptr.hasdodges(bell(b))

    def has_places(self, int b):
        return self.thisptr.hasplaces(bell(b))

    def symmetry_point(self, b=None):
        cdef int result

        if b is None:
            result = self.thisptr.symmetry_point()
        else:
            result = self.thisptr.symmetry_point(bell(b))

        if result == -1:
            return False

        return result

    def max_blows(self):
        return self.thisptr.maxblows()

    def append(self, c):
        if isinstance(c, Change):
            self.thisptr.push_back(deref((<Change>c).thisptr))
        elif isinstance(c, unicode):
            self.thisptr.push_back(<string>(c.encode()))
        elif isinstance(c, bytes):
            self.thisptr.push_back(<string>c)
        else:
            raise TypeError("Cannot append {type} to ringing.Method".format(
                type=type(c).__name__
            ))

    def __len__(self):
        return self.size

    def __getitem__(self, int x):
        cdef Change result = Change()

        if 0 <= x < self.size:
            result.thisptr[0] = deref(self.thisptr)[x]
            return result
        else:
            raise IndexError('ringing.Method index out of range')

    def __setitem__(self, int x, y):
        cdef Change cy = Change(y)

        if 0 <= x < self.size:
            deref(self.thisptr)[x] = deref(cy.thisptr)
        else:
            raise IndexError('ringing.Method index out of range')
