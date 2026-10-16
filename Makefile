.PHONY: sync build build-dist check docs clean

sync:
	uv sync --all-groups --locked

build:
	uv sync --reinstall-package ringing-lib

build-dist:
	uv build

check:
	uv run --locked pytest

docs:
	make -C docs html

clean:
	rm -rf dist
	rm -f src/ringing.cpp
	rm -f src/ringing.*.so
	rm -rf src/ringing_lib.egg-info/
	make -C docs clean
