cdef class Method:

    cdef method *thisptr

    def __cinit__(self, input=None, int bells=0, name='Untitled'):
        cdef string name_string

        # Validate bells parameter
        if not (0 <= bells <= 256):
            raise ValueError('Number of bells must be between 0 and 256')

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
