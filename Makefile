.PHONY: default build build-dist check clean clean-docs docs stubs sync wheels

default: sync

build:
	uv sync --reinstall-package ringing-lib

build-dist: stubs
	uv build

check:
	uv run --locked pytest

clean:
	rm -rf dist
	rm -f ringing/__init__.pyi
	rm -f ringing/_ringing.cpp
	rm -f ringing/_ringing.*.so
	rm -rf ringing_lib.egg-info/

clean-docs:
	make -C docs clean

docs:
	make -C docs html

ringing/__init__.pyi: ringing/_ringing.pyx $(wildcard ringing/*.pxd) $(wildcard ringing/*.pxi)
	uv run --locked stubgen-pyx \
	    --file $< \
	    --output-file $@ \
	    --replace-defaults-with-ellipsis

stubs: ringing/__init__.pyi

sync:
	uv sync --all-groups --locked

wheels:
	uv run --locked cibuildwheel --output-dir dist
