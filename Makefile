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
	rm -f ringing.*.so
	rm -f ringing/ringing.cpp
	rm -f ringing/ringing.pyi
	rm -rf ringing_lib.egg-info/

clean-docs:
	make -C docs clean

docs:
	make -C docs html

ringing/ringing.pyi: ringing/ringing.pyx $(wildcard ringing/*.pxd) $(wildcard ringing/*.pxi)
	uv run --locked stubgen-pyx \
	    --file $< \
	    --output-file $@ \
	    --replace-defaults-with-ellipsis

stubs: ringing/ringing.pyi

sync:
	uv sync --all-groups --locked
