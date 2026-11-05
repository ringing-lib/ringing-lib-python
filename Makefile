.PHONY: default build build-dist check clean clean-docs docs stubs sync wheels

SOURCE_FILES = ringing/_ringing.pyx $(wildcard ringing/*.pxd) $(wildcard ringing/*.pxi)

default: sync

build: ringing/_ringing.cpp

build-dist: build stubs
	uv build --sdist

check: build
	uv run --locked pytest

clean:
	rm -rf dist
	rm -f ringing/__init__.pyi
	rm -f ringing/_ringing.cpp
	rm -f ringing/_ringing.*.so
	rm -rf ringing_lib.egg-info/

clean-docs:
	make -C docs clean

docs: build
	make -C docs html

ringing/__init__.pyi: $(SOURCE_FILES)
	uv run --locked stubgen-pyx \
	    --file $< \
	    --output-file $@ \
	    --replace-defaults-with-ellipsis

ringing/_ringing.cpp: $(SOURCE_FILES)
	uv sync --reinstall-package ringing-lib

stubs: ringing/__init__.pyi

sync:
	uv sync --locked

wheels: stubs
	uv run --locked cibuildwheel --output-dir dist
