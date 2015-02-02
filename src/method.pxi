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

    property name:
        def __get__(self):
            if PY_MAJOR_VERSION < 3:
                return <bytes>self.thisptr.name()
            else:
                return (<bytes>self.thisptr.name()).decode()

        def __set__(self, value):
            if isinstance(value, unicode):
                self.thisptr.name(<string>(value.encode()))
            elif isinstance(value, bytes):
                self.thisptr.name(<string>value)
            else:
                raise TypeError('Cannot convert {type} to string'.format(
                    type=type(input).__name__
                ))

    def full_name(self):
        if PY_MAJOR_VERSION < 3:
            return <bytes>self.thisptr.fullname()
        else:
            return (<bytes>self.thisptr.fullname()).decode()

    @staticmethod
    def stage_name(int bells):
        if 0 <= bells <= MAX_BELL_NUMBER:
            if PY_MAJOR_VERSION < 3:
                return <bytes>method.stagename(bells)
            else:
                return (<bytes>method.stagename(bells)).decode()
        else:
            raise ValueError('Number of bells out of range')

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

    def is_symmetric(self, b=None):
        if b is None:
            return self.thisptr.issym()
        else:
            if 0 <= b < self.bells:
                return self.thisptr.issym(bell(b))
            else:
                raise IndexError('Bell number out of range')

    def is_palindromic(self, b=None):
        if self.size % 2:
            raise ValueError('Method contains an odd number of changes')

        if b is None:
            return self.thisptr.ispalindromic()
        else:
            if 0 <= b < self.bells:
                return self.thisptr.ispalindromic(bell(b))
            else:
                raise IndexError('Bell number out of range')

    def is_double(self):
        return self.thisptr.isdouble()

    def is_regular(self):
        return self.thisptr.isregular()

    def hunt_bells(self):
        return self.thisptr.huntbells()

    def leads(self):
        return self.thisptr.leads()

    def is_plain(self, b=0):
        if 0 <= b < self.bells:
            return self.thisptr.isplain(bell(b))
        else:
            raise IndexError('Bell number out of range')

    def has_dodges(self, int b):
        if 0 <= b < self.bells:
            return self.thisptr.hasdodges(bell(b))
        else:
            raise IndexError('Bell number out of range')

    def has_places(self, int b):
        if 0 <= b < self.bells:
            return self.thisptr.hasplaces(bell(b))
        else:
            raise IndexError('Bell number out of range')

    def lh_code(self):
        if PY_MAJOR_VERSION < 3:
            return <bytes>self.thisptr.lhcode()
        else:
            return (<bytes>self.thisptr.lhcode()).decode()

    def symmetry_point(self, b=None):
        cdef int result

        if self.size % 2:
            raise ValueError('Method contains an odd number of changes')

        if b is None:
            result = self.thisptr.symmetry_point()
        else:
            if 0 <= b < self.bells:
                result = self.thisptr.symmetry_point(bell(b))
            else:
                raise IndexError('Bell number out of range')

        if result == -1:
            return False

        return result

    def max_blows(self):
        return self.thisptr.maxblows()

    def format(self, **kwargs):
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
            raise ValueError('Cannot use symmetry flags with methods '
                             'containing an odd number of changes')

        if PY_MAJOR_VERSION < 3:
            return <bytes>self.thisptr.format(format)
        else:
            return (<bytes>self.thisptr.format(format)).decode()

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

    def __richcmp__(x, y, int op):
        cdef method mx
        cdef method my

        try:
            mx = deref(Method(x).thisptr)
            my = deref(Method(y).thisptr)
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

    def __str__(self):
        if PY_MAJOR_VERSION < 3:
            return self.__bytes__()
        else:
            return self.__unicode__()

    def __bytes__(self):
        return <bytes>self.thisptr.fullname()

    def __unicode__(self):
        return (<bytes>self.thisptr.fullname()).decode()

    def __repr__(self):
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
