import os
from setuptools import setup, Extension
import sys

from Cython.Build import cythonize


# Don't run any setup tasks if we're running on readthedocs.org.
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    sys.exit()


cythonize(Extension('*', ['src/*.pyx'], language='c++'))


setup(
    name='ringing-lib',
    version='0.1.0',
    author='Leigh Simpson',
    author_email='code@simpleigh.com',
    url='http://github.com/simpleigh/ringing-lib-python',
    description='Python wrapper for the Ringing Class Library',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    license='GPL',
    ext_modules=[Extension('ringing',
        language='c++',
        sources=['src/ringing.cpp', 'src/row.cpp', 'src/change.cpp'],
        libraries=['ringing', 'ringingcore'],
    )],
    test_suite='tests',
)
