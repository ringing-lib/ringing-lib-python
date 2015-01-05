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
