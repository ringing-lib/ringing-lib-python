#!/usr/bin/env bash

# Query version numbers to aid debugging
git --version
make --version
g++ --version

# Check out the commit configured in `pyproject.toml`
git clone \
    --depth 1 \
    --revision ${RINGING_LIB_SHA} \
    https://github.com/ringing-lib/ringing-lib
cd ringing-lib

# Compile and install
SUBDIRS='ringing utils'  # only build the libraries, not the apps
make SUBDIRS="${SUBDIRS}"
find . -type f -name '*.so' | xargs strip --strip-unneeded --verbose
make SUBDIRS="${SUBDIRS}" install
