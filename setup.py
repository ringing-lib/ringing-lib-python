from pathlib import Path

from Cython.Build import cythonize
from setuptools import Extension, setup

setup(
    ext_modules=cythonize(
        [
            Extension(
                'ringing._ringing',
                ['ringing/_ringing.pyx'],
                language='c++',
                libraries=['ringing', 'ringingcore', 'ringingutils'],
            ),
        ],
        include_path=[Path(__file__).parent / 'ringing'],
    ),
)
