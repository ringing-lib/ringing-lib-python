import os
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext
import sys


# Don't run any setup tasks if we're running on readthedocs.org.
if os.environ.get('READTHEDOCS', None) == 'True':
    sys.exit()


# Detect whether Cython is installed.
try:
    import Cython
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False


# Override build_ext to add --static option.
class build_ext(_build_ext):

    user_options = _build_ext.user_options + [
        ('static', None, 'statically link the Ringing Class Library'),
    ]

    def initialize_options(self):
        _build_ext.initialize_options(self)
        self.static = False


# ... but then grab it straight out of sys.argv hackhackhackhack
if '--static' in sys.argv:
    EXTENSION_OPTIONS = {
        'language': 'c++',
        'extra_link_args': [
            '-Wl,-Bstatic',
            '-lringing',
            '-lringingcore',
            '-Wl,-Bdynamic',
        ],
    }
else:
    EXTENSION_OPTIONS = {
        'language': 'c++',
        'libraries': ['ringing', 'ringingcore'],
    }


if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize([
        Extension('ringing', ['src/ringing.pyx'], **EXTENSION_OPTIONS),
    ])
else:
    extensions = [
        Extension('ringing', ['src/ringing.cpp'], **EXTENSION_OPTIONS)
    ]


with open('README.rst') as file:
    long_description = file.read()


setup(
    name='ringing-lib',
    version='0.1.0',
    author='Leigh Simpson',
    author_email='code@simpleigh.com',
    url='http://github.com/simpleigh/ringing-lib-python',
    description='Python wrapper for the Ringing Class Library',
    long_description=long_description,
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
    ext_modules=extensions,
    test_suite='tests',
    cmdclass={'build_ext': build_ext},
)
