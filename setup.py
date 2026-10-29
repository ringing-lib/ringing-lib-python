import os
from pathlib import Path
from typing import Any

from Cython.Build import cythonize
from setuptools import Extension, setup

extension_kwargs: dict[str, Any] = {}

if os.environ.get('READTHEDOCS') == 'True':
    lib_dir = Path(__file__).parent / '.ringing-lib'
    extension_kwargs['include_dirs'] = [str(lib_dir / 'include')]
    extension_kwargs['library_dirs'] = [str(lib_dir / 'lib')]

setup(
    ext_modules=cythonize(
        [
            Extension(
                'ringing._ringing',
                ['ringing/_ringing.pyx'],
                language='c++',
                libraries=['ringing', 'ringingcore', 'ringingutils'],
                **extension_kwargs,
            ),
        ],
        include_path=[Path(__file__).parent / 'ringing'],
    ),
)
