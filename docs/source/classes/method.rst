Methods
=======

.. currentmodule:: ringing

The Ringing Class Library provides many useful functions for dealing with
methods, finding information about them and classifying them.

A *method* consists of one block of changes which is repeated over and over
again; this is called a *lead*. If, at the end of one lead, every bell is in a
different position, then the method is called a *principle* and the leads are
called *divisions*. Any bells in a method which end up in the same place at the
end of a lead are called *hunt bells*.

The Ringing Class Library defines a :class:`Method` object which is simply a
block of changes and which provides a large range of member functions. Many of
these are used for finding out things about the method, such as the number of
leads in the plain course, the type of method, the full name and so on.

The Method Class
----------------

The :class:`Method` class represents a method by storing the changes which make
up one lead of the method.

A method may have a name, which is a string variable. This name is the *base
name* of the method, that is, it is the name without any extra bits such as
"Surprise" or "Triples". For example, the base name of Plain Bob Major is simply
"Plain". The parts of the name other than the base can be worked out by the
Ringing Class Library.

.. class:: Method([spec=None], [bells=0], [name='Untitled'])
      
      Constructs a Method.
      
      Methods may be constructed in a variety of ways::
         
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
      
      ===============  =================================================
      Operation        Result
      ===============  =================================================
      ``c in m``       ``True`` if an item of *m* is equal to *c*, else
                       ``False``
      ``c not in m``   ``False`` if an item of *m* is equal to *c*, else
                       ``True``
      ``m[i]``         *i*\ th change of *m*, origin 0
      ``m[i] = c``     sets *i*\ th change of *m*
      ``len(m)``       length (:attr:`size`) of *m*
      ``list(m)``      list of changes in *m*
      ``m.append(c)``  appends *c* to the end of the method
      ===============  =================================================
      
      The syntax of the place notation is as follows: place notation consists of
      a sequence of blocks, which are delimited by commas. Each block is a
      sequence of changes, with ``X`` or ``-`` meaning a cross change. Changes
      other than cross changes are separated by full stops. A block may
      optionally be preceded by an ampersand ``&``, which means that the entire
      block, except the last change, is repeated backwards. All other characters
      are ignored.
      
      :param spec: Specification for constructing the method.
         This might be:
         
         *  Nothing. Constructs a zero-length method.
         *  Another method. Constructs a copy.
         *  An integer length. Constructs a method of the specified length.
         *  A string (unicode or bytes) place notation.
      :type spec: :class:`Method` or int or string
      :param int bells: number of bells
      :param string name: base name of the method
      
      .. method:: __lt__(method)
      .. method:: __le__(method)
      .. method:: __eq__(method)
      .. method:: __ne__(method)
      .. method:: __gt__(method)
      .. method:: __ge__(method)
         
         Compares a method to another.
         
         :param method: value to compare
         :type method: :class:`Method`
         :return: result
         :rtype: boolean
      
      .. attribute:: size
         
         Number of changes in a lead of the method::
            
            >>> from ringing import Method
            >>> Method('&-1-1-1,2', 6).size
            12
      
      .. attribute:: length
         
         Synonym for :attr:`size`.
      
      .. attribute:: bells
         
         Number of bells on which the method is defined::
            
            >>> from ringing import Method
            >>> Method('&-1-1-1,2', 6).bells
            6
      
      .. attribute:: name
         
         Base name of the method. Note that this may be an empty string, for
         example in Little Bob.
         Unlike many attributes in this library, a new value may be assigned to
         this attribute::
            
            >>> from ringing import Method
            >>> m = Method('&-1-1-1,2', 6)
            >>> m.name
            'Untitled'
            >>> m.name = 'Plain'
            >>> m
            Method('&-16-16-16,12', 6, 'Plain')
      
      .. method:: append(change)
         
         Adds a change to the end of the method. The *change* may be provided as
         a :class:`Change` object or a string containing the place notation to
         be added.
         
         :param change: change to be added
         :type change: :class:`Change` or string
      
      .. method:: lead_head()
         
         Returns the first lead head of the method::
            
            >>> from ringing import Method
            >>> Method('&-1-1-1,2', 6).lead_head()
            Row('135264')
         
         :return: first lead head
         :rtype: :class:`Row`
      
      .. method:: leads()
         
         Returns the number of leads in the plain course of the method.
         This is equivalent to the order of the lead-head row::
            
            >>> from ringing import Method
            >>> Method('&-1-1-1,2', 6).leads()
            5
            >>> Method('&-1-1-1,2', 6).lead_head().order()
            5
         
         :return: number of leads
         :rtype: int
      
      .. method:: is_regular()
         
         Returns ``True`` if the method is regular (that is, it has Plain Bob
         lead heads), or ``False`` otherwise.
         
         :return: whether the method is regular
         :rtype: boolean
      
      .. method:: lh_code()
         
         Returns the standard code for the lead end and lead head of the
         method::
            
            >>> from ringing import Method
            >>> Method('&-1-1-1,2', 6).lh_code()
            'a'
         
         :return: lead head code
         :rtype: string
      
      .. method:: hunt_bells()
         
         Returns the number of hunt bells in the method::
            
            >>> from ringing import Method
            >>> Method('&-1-1-1,2', 6).hunt_bells()
            1
         
         :return: number of hunt bells
         :rtype: int
      
      .. method:: is_symmetric([bell])
         
         Returns ``True`` if the method is symmetrical about the half lead (and
         has an even number of changes in the lead), or ``False`` otherwise.
         If a *bell* number is specified, returns ``True`` if the path of that
         bell in a lead of the method is symmetrical about the half lead, or
         ``False`` otherwise.
         
         :param bell: bell to check
         :type bell: :class:`Bell` or string or int
         :return: whether the method is symmetric
         :rtype: boolean
      
      .. method:: is_palindromic([bell])
         
         Returns ``True`` if the method is symmetrical about any point (and has
         an even number of changes in the lead), or ``False`` otherwise.
         If a *bell* number is specified, returns ``True`` if the path of that
         bell in a lead of the method is symmetrical about any point, or
         ``False`` otherwise.
         
         :param bell: bell to check
         :type bell: :class:`Bell` or string or int
         :return: whether the method is symmetric
         :rtype: boolean
      
      .. method:: is_double()
         
         Returns ``True`` if the method is double, or ``False`` otherwise. Note
         that double does not imply symmetrical.
         
         :return: whether the method is double
         :rtype: boolean
      
      .. method:: max_blows()
         
         Returns the maximum consecutive blows made in any place in this method.
         (If the method has one bell fixed throughout, the lead length is
         returned.)::
            
            >>> from ringing import Method
            >>> Method('&-1-1-1,2', 6).max_blows()
            2
         
         :return: maximum consecutive blows
         :rtype: int
      
      .. method:: is_plain([bell])
         
         Returns ``True`` if *bell* plain hunts for the whole lead of the
         method, or ``False`` otherwise.
         
         If *bell* is not provided then the treble path is checked.
         
         :param bell: bell to check
         :type bell: :class:`Bell` or string or int
         :return: whether the bell plain hunts
         :rtype: boolean
      
      .. method:: has_dodges(bell)
         
         Returns ``True`` if *bell* dodges during the lead, or ``False``
         otherwise.
         
         :param bell: bell to check
         :type bell: :class:`Bell` or string or int
         :return: whether the bell dodges
         :rtype: boolean
      
      .. method:: has_places(bell)
         
         Returns ``True`` if *bell* makes any internal places during the lead,
         or ``False`` otherwise.
         
         :param bell: bell to check
         :type bell: :class:`Bell` or string or int
         :return: whether the bell makes internal places
         :rtype: boolean
      
      .. method:: full_name()
         
         Assembles the full name of the method::
            
            >>> from ringing import Method
            >>> Method('&-1-1-1,2', 6, 'Plain').full_name()
            'Plain Bob Minor'
         
         The full name consists of:
         *  the base name of the method;
         *  the word "Little", if appropriate;
         *  the class of the method, or none if it is a principle;
         *  the stage (number of bells) of the method
         
         Note that Grandsire, Union and their related methods are treated
         specially: the full name of these methods does not include their class,
         nor in the case of Little Grandsire does it contain "Little".
         
         :return: full name
         :rtype: string
      
      .. staticmethod:: stage_name(bells)
         
         Returns a string describing the stage of *bells* bells: thus
         "``Minimus``", "``Doubles``", and so on::
            
            >>> from ringing import Method
            >>> Method.stage_name(8)
            'Major'
         
         For stages above Sixteen, the number is given in digits.
         
         :param int bells: number of bells
         :return: stage name
         :rtype: string
      
      .. method:: format(**kwargs)
         
         Formats the method's place notation into a string::
            
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
