.PHONY: sync build check docs clean

sync:
	uv sync --all-groups --locked

build:
	uv build

check:
	uv run --locked python -m unittest discover -s tests -v

docs:
	make -C docs html

clean:
	rm -rf dist
	rm -f src/ringing.cpp
	rm -f src/ringing.*.so
	rm -rf src/ringing_lib.egg-info/
	make -C docs clean
