from typing import TypeAlias


MethodSpec: TypeAlias = Method | int | str | bytes | None


cdef class Method:

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

    property name:
        def __get__(self) -> str:
            return (<bytes>self.thisptr.name()).decode()

        def __set__(self, value: str | bytes) -> None:
            if isinstance(value, str):
                self.thisptr.name(<string>(value.encode()))
            elif isinstance(value, bytes):
                self.thisptr.name(<string>value)
            else:
                raise TypeError('Cannot convert {type} to string'.format(
                    type=type(input).__name__,
                ))

    def full_name(self) -> str:
        return (<bytes>self.thisptr.fullname()).decode()

    @staticmethod
    def stage_name(int bells) -> str:
        if 0 <= bells <= MAX_BELL_NUMBER:
            return (<bytes>method.stagename(bells)).decode('ascii')
        else:
            raise ValueError('Number of bells out of range')

    property size:
        def __get__(self) -> int:
            return self.thisptr.size()

    property length:
        def __get__(self) -> int:
            return self.thisptr.length()

    property bells:
        def __get__(self) -> int:
            return self.thisptr.bells()

    def lead_head(self) -> Row:
        cdef Row result = Row()
        result.thisptr[0] = self.thisptr.lh()
        return result

    def is_symmetric(self, b: BellSpec = None) -> bool:
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
        return self.thisptr.isdouble()

    def is_regular(self) -> bool:
        return self.thisptr.isregular()

    def hunt_bells(self) -> int:
        return self.thisptr.huntbells()

    def leads(self) -> int:
        return self.thisptr.leads()

    def is_plain(self, b: BellSpec = 0) -> bool:
        cdef bell bb = deref(Bell(b).thisptr)

        if <int>bb < self.bells:
            return self.thisptr.isplain(bb)
        else:
            raise IndexError('Bell number out of range')

    def has_dodges(self, b: BellSpec) -> bool:
        cdef bell bb = deref(Bell(b).thisptr)

        if <int>bb < self.bells:
            return self.thisptr.hasdodges(bb)
        else:
            raise IndexError('Bell number out of range')

    def has_places(self, b: BellSpec) -> bool:
        cdef bell bb = deref(Bell(b).thisptr)

        if <int>bb < self.bells:
            return self.thisptr.hasplaces(bb)
        else:
            raise IndexError('Bell number out of range')

    def lh_code(self) -> str:
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
        return self.thisptr.maxblows()

    def format(self, **kwargs) -> str:
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
