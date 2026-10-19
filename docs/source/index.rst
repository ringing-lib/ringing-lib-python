lib-ringing-python Documentation
================================

**Wrapper for the Ringing Class Library**.

.. |main| image:: https://img.shields.io/github/actions/workflow/status/ringing-lib/ringing-lib-python/build.yml?branch=main
   :alt: Build Status - main branch
   :target: https://github.com/ringing-lib/ringing-lib-python/actions/workflows/build.yml

About
-----

This package contains Python bindings for the
`Ringing Class Library <http://ringing-lib.github.io/>`_.

*  GitHub: https://github.com/ringing-lib/ringing-lib-python
*  Supports: CPython versions 3.11 to 3.15.
*  |main|

.. toctree::
   :maxdepth: 1

   changelog

Installation
------------

1. **Install the Ringing Class Library**.

   You can download the latest source from
   `GitHub <https://github.com/ringing-lib/ringing-lib>`_.
   After obtaining appropriate prerequisites you can configure and install.
   Within the Ringing Class Library source tree:

   .. code-block:: bash

      make
      make install

   Run :command:`make install` as root.

2. **Install Using pip**

   Install directly from
   `PyPI <https://pypi.python.org/pypi/ringing-lib/>`_:

   .. code-block:: bash

      pip install ringing-lib

   .. note::

      This is a C++ Python extension: you will need a working compiler with
      access to Python headers in order to build it.

Alternatively, to build from source:

2. **Install dependencies**.

   Use uv to install the required dependencies:

   .. code-block:: bash

      make sync

3. **Compile the Python extension**.

   Build the extension:

   .. code-block:: bash

      make build

4. (Optional) **Run Tests**.

   Run the included tests:

   .. code-block:: bash

      make check

5. (Optional) **Build package and wheels**.

   Build a package for distribution:

   ... code-block:: bash

      make build-dist

Class Documentation
-------------------

.. module:: ringing

.. toctree::
   :maxdepth: 2

   classes/bell
   classes/row
   classes/change
   classes/method

Licence
-------

This software is copyright:

   Copyright © 2014-2026  Leigh Simpson <code@simpleigh.com>

   This library is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This library is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this library.  If not, see <http://www.gnu.org/licenses/>.

This documentation is copyright:

   Copyright © 2014-2026  Leigh Simpson <code@simpleigh.com>

   Permission is granted to copy, distribute and/or modify this document under
   the terms of the GNU Free Documentation License, Version 1.1 or any later
   version published by the Free Software Foundation; with no Invariant
   Sections, with no Front-Cover Texts, and with no Back-Cover Texts. A copy of
   the license is included in the section entitled “GNU Free Documentation
   License”.

In addition, large portions of the class documentation are taken directly from
the manual for the Ringing Class Library, which is also copyright:

   Copyright © 2001-26 Martin Bright, Mark Banner and Richard Smith

.. toctree::
   :maxdepth: 1

   licence

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
