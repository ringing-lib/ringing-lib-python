import os
from setuptools import setup, Extension
import sys


BASE_DIR = os.path.dirname(__file__)


# Don't run any setup tasks if we're running on readthedocs.org.
if os.environ.get('READTHEDOCS', None) == 'True':
    sys.exit()


EXTENSION_OPTIONS = {
    'language': 'c++',
    'libraries': ['ringing', 'ringingcore'],
}


# Detect whether Cython is installed.
try:
    from Cython.Build import cythonize
except ImportError:
    extensions = [
        Extension('ringing', ['src/ringing.cpp'], **EXTENSION_OPTIONS)
    ]
else:
    extensions = cythonize([
        Extension('ringing', ['src/ringing.pyx'], **EXTENSION_OPTIONS),
    ])


with open(os.path.join(BASE_DIR, 'VERSION')) as version_file:
    version = version_file.read().strip()


with open('README.rst') as file:
    long_description = file.read()


setup(
    name='ringing-lib',
    version=version,
    author='Leigh Simpson',
    author_email='code@simpleigh.com',
    url='http://github.com/simpleigh/ringing-lib-python',
    description='Python wrapper for the Ringing Class Library',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
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
)
