import os

from Cython.Build import cythonize
from setuptools import Extension, setup


# Don't run any setup tasks if we're running on readthedocs.org.
if os.environ.get('READTHEDOCS', None) == 'True':
    setup()
else:
    setup(
        ext_modules=cythonize([
            Extension(
                'ringing',
                ['ringing/ringing.pyx'],
                language='c++',
                libraries=['ringing', 'ringingcore', 'ringingutils'],
            ),
        ]),
    )
