.PHONY: default build build-dist check clean clean-docs docs stubs sync

default: sync

build:
	uv sync --reinstall-package ringing-lib

build-dist: stubs
	uv build

check:
	uv run --locked pytest

clean: clean-docs
	rm -rf dist
	rm -f src/ringing.cpp
	rm -f src/ringing.pyi
	rm -f src/ringing.*.so
	rm -rf src/ringing_lib.egg-info/

clean-docs:
	make -C docs clean

docs:
	make -C docs html

src/ringing.pyi: src/ringing.pyx $(wildcard src/*.pxd) $(wildcard src/*.pxi)
	uv run --locked stubgen-pyx \
	    --file $< \
	    --output-file $@ \
	    --replace-defaults-with-ellipsis

stubs: src/ringing.pyi

sync:
	uv sync --all-groups --locked
